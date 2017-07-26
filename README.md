# Logs Analysis Website
### _by Arvind Rathee_
Logs Analysis project, part of the Udacity [Full Stack Web Developer Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004).

## What is this project about?
This project analyze the log data by querying SQL and outputs the data into a text file. This project runs directly from command line and does not take any input from the user.

## Database and its Adapter for Python
_PostgreSQL_ along with _Psycopg 2_ most popular PostgreSQL database adapter for the Python programming language.

### Project Content
- main.py - This file contain code for querying the database and processing it.
- out.txt - This file contains the output of main.py
- newsdata.zip - This contain the databse file that is used to import database.

## Requirements for the program to run
- PostgreSQL - [Download Here](https://www.postgresql.org/download/)
- Python 3 - [Download Here](https://www.python.org/downloads/)
- Psycopg 2 - install it using ```python
			  pip install psycopg2 
			  ```


## How to run the program?

Download the project zip file to you computer and unzip the file. Or clone this
repository to your desktop.

Navigate to the project directory.

Unzip newsdata.zip and run following code to import the newsdata.sql
```SQL
psql -f newsdata.sql -U username
```
Above code will prompt for password enter the password

Now database 'news' has been created containg tables
- articles
- log
- authors

Run python program using command line or terminal
```Shell
python main.py
```

A file named out.txt is created in the directory with output of the program in it.

## Notes
- In main.py you must replace user and password with your own while connecting to the database.