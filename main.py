#!/usr/bin/python3

import psycopg2


# File is created for storing the output
fh = open("out.txt", 'w')


def problem1():
    '''This function outputs three most viewed article of all time'''

    # Connection to the 'news' database is made
    # User and pass maybe different for different computers
    conn = psycopg2.connect("dbname=news user=vagrant password=pass")
    # Open a cursor to perform database operations
    cur = conn.cursor()
    # SQL query for finding most viwed article
    cur.execute("""SELECT articles.title, COUNT(log.path)
                   FROM log, articles
                   WHERE REPLACE(path, '/article/', '') = articles.slug
                   GROUP BY articles.title
                   ORDER BY count DESC
                   LIMIT 3;""")
    # Fetches the output of above query into a python object
    output = cur.fetchall()
    # Heading of the output so that it can be aranged properly
    fh.write("|{0:^40}|{1:^18}|\n".format('Article Title', 'Views'))
    fh.write("|----------------------------------------+------------------|")
    # Iterate through output of SQL and write them to file
    for each in range(len(output)):
        title = output[each][0]
        views = str(output[each][1])
        fh.write("\n|{0:^40}|{1:^18}|".format(title, views))
    fh.write('\n\n\n\n')
    # Close communication with the database
    conn.close()


def problem2():
    '''This function outputs most popular author of all time'''

    conn = psycopg2.connect("dbname=news user=vagrant password=pass")
    cur = conn.cursor()
    cur.execute("""SELECT authors.name, COUNT(articles.author)
                   FROM log, articles, authors
                   WHERE REPLACE(log.path, '/article/', '') = articles.slug
                   AND articles.author = authors.id
                   GROUP BY authors.name
                   ORDER BY count DESC;""")
    output = cur.fetchall()
    fh.write("|{0:^40}|{1:^18}|\n".format('Author Name', 'Views'))
    fh.write("|----------------------------------------+------------------|")
    for each in range(len(output)):
        author = output[each][0]
        views = str(output[each][1])
        fh.write("\n|{0:^40}|{1:^18}|".format(author, views))
    fh.write('\n\n\n\n')
    conn.close()


def problem3():
    '''This function outputs the days when percent error was more than 1%'''

    conn = psycopg2.connect("dbname=news user=vagrant password=pass")
    cur = conn.cursor()
    cur.execute("""SELECT to_char(log.time::date, 'YYYY-MM-DD'),
                   (new.total*100)/(COUNT(log.time::date)) as percent
                   FROM (SELECT time::date, COUNT(time::date) as total
                         FROM log WHERE status != '200 OK'
                         GROUP BY time::date
                         ORDER BY total DESC) as new, log
                   WHERE new.time::date = log.time::date
                   GROUP BY to_char(log.time::date, 'YYYY-MM-DD'), new.total
                   ORDER BY percent DESC;""")
    output = cur.fetchall()
    fh.write("|{0:^40}|{1:^18}|\n".format('Date', 'Percentage'))
    fh.write("|----------------------------------------+------------------|")
    for each in range(len(output)):
        if output[each][1] > 1:
            date = output[each][0]
            percent = str(output[each][1]) + '%'
            fh.write("\n|{0:^40}|{1:^18}|".format(date, percent))
    fh.write('\n\n\n\n')
    conn.close()

fh.write("1. What are the most popular three articles of all time?\n\n")
# Calling problem1
problem1()

fh.write("2. Who are the most popular article authors of all time?\n\n")
# Calling problem2
problem2()

fh.write("3. On which days did more than 1% of requests lead to errors?\n\n")
# Calling problem3
problem3()

# Closing the file
fh.close()
