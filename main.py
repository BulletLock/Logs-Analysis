#!/usr/bin/python3

import psycopg2


def db_connect(db_name, username, password):
    """This funcion connects to the database and open a cursor"""

    try:
        # Connection to the database is made
        conn = psycopg2.connect("""dbname={} user={} password={}
                                """.format(db_name, username, password))
        # Open a cursor to perform database operations
        cur = conn.cursor()
        return conn, cur
    except psycopg2.Error as e:
        print("Unable to connect to database")
        # Raise the error
        raise e


def process_query(sql_query):
    """This function processes sql query and ouput the result"""

    # User and pass maybe different for different computers
    conn, cur = db_connect('news', 'vagrant', 'pass')
    # SQL query for finding most viwed article
    cur.execute(sql_query)
    # Fetches the output of above query into a python object
    output = cur.fetchall()
    # Close the cursor
    cur.close()
    # Close connection to the database
    conn.close()
    return output


def top_articles(query):
    """This function outputs three most viewed article of all time"""

    output = process_query(query)
    fh.write("|{0:^40}|{1:^18}|\n".format('Article Title', 'Views'))
    fh.write("|----------------------------------------+------------------|")
    # Iterate through output of SQL and write them to file
    for each in range(len(output)):
        title = output[each][0]
        views = str(output[each][1])
        fh.write("\n|{0:^40}|{1:^18}|".format(title, views))
    fh.write('\n\n\n\n')


def top_authors(query):
    """This function outputs most popular author of all time"""

    output = process_query(query)
    fh.write("|{0:^40}|{1:^18}|\n".format('Author Name', 'Views'))
    fh.write("|----------------------------------------+------------------|")
    for each in range(len(output)):
        author = output[each][0]
        views = str(output[each][1])
        fh.write("\n|{0:^40}|{1:^18}|".format(author, views))
    fh.write('\n\n\n\n')


def most_error_day(query):
    """This function outputs the days when percent error was more than 1%"""

    output = process_query(query)
    fh.write("|{0:^40}|{1:^18}|\n".format('Date', 'Percentage'))
    fh.write("|----------------------------------------+------------------|")
    for each in range(len(output)):
        if output[each][1] > 1:
            date = output[each][0]
            percent = str(output[each][1]) + '%'
            fh.write("\n|{0:^40}|{1:^18}|".format(date, percent))
    fh.write('\n\n\n\n')

if __name__ == '__main__':
    # This code makes sure that this file was ran directly, not imported.

    # File is created for storing the output
    fh = open("out.txt", 'w')

    fh.write("1. What are the most popular three articles of all time?\n\n")
    # Calling top_articels and passing the query
    top_articles("""SELECT articles.title, COUNT(log.path)
                    FROM log, articles
                    WHERE REPLACE(path, '/article/', '') = articles.slug
                    GROUP BY articles.title
                    ORDER BY count DESC
                    LIMIT 3;""")

    fh.write("2. Who are the most popular article authors of all time?\n\n")
    # Calling top_authors and passing the query
    top_authors("""SELECT authors.name, COUNT(articles.author)
                   FROM log, articles, authors
                   WHERE REPLACE(log.path, '/article/', '') = articles.slug
                   AND articles.author = authors.id
                   GROUP BY authors.name
                   ORDER BY count DESC;""")

    fh.write("3. When did more than 1% of requests lead to errors?\n\n")
    # Calling most_error_day and passing the query
    most_error_day("""SELECT to_char(log.time::date, 'YYYY-MM-DD'),
                       (new.total*100)/(COUNT(log.time::date)) as percent
                       FROM (SELECT time::date, COUNT(time::date) as total
                             FROM log WHERE status != '200 OK'
                             GROUP BY time::date
                             ORDER BY total DESC) as new, log
                       WHERE new.time::date = log.time::date
                       GROUP BY to_char(log.time::date, 'YYYY-MM-DD'),
                       new.total ORDER BY percent DESC;""")

    # Closing the file
    fh.close()
