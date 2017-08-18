#!/usr/bin/env python2.7
# python file for specific SQL queries

import psycopg2

DATABASE = "dbname=news"
OUTPUT = "output.txt"
f = None


def db_connect():
    """ Creates and returns a connection to the database defined by DBNAME,
        as well as a cursor for the database.

        Returns:
            db, c - a tuple. The first element is a connection to the database.
                    The second element is a cursor for the database.
    """

    db = psycopg2.connect(DATABASE)
    c = db.cursor()
    return db, c


def execute_query(query):
    """execute_query takes an SQL query as a parameter.
        Executes the query and returns the results as a list of tuples.
        args:
            query - an SQL query statement to be executed.

       returns:
           A list of tuples containing the results of the query.
    """

    db, c = db_connect()
    c.execute(query)
    return c.fetchall()


def print_top_articles():
    """Prints out the top 3 articles of all time."""
    query = '''
    SELECT articles.title, log_new.views
    FROM articles JOIN
        (SELECT path, count(*) AS views
        FROM log
        WHERE (status = '200 OK')
        AND path != '/'
        GROUP BY path) AS log_new
    ON log_new.path = concat('/article/', articles.slug)
    ORDER BY log_new.views DESC
    LIMIT 3
    '''
    results = execute_query(query)

    q = "1. What are the most popular three articles of all time? \n"
    print q
    f.write(q)

    for item in results:
        string1 = "{} -- {} views \n".format(item[0], item[1])
        print string1
        f.write(string1)
    f.write("\n")


def print_top_authors():
    """Prints a list of authors ranked by article views."""
    query = '''
    SELECT authors.name, sum(articles.views)
    FROM authors JOIN
        (SELECT articles.author, log_new.views
        FROM articles JOIN
            (SELECT path, count(*) AS views
            FROM log
            WHERE (status = '200 OK')
            AND path != '/'
            GROUP BY path) AS log_new
        ON log_new.path = concat('/article/', articles.slug)
        ORDER BY log_new.views DESC) AS articles
    ON authors.id = articles.author
    GROUP BY authors.id
    '''
    results = execute_query(query)

    q = "2. Who are the most popular article authors of all time? \n"
    print q
    f.write(q)

    for author in results:
        string2 = "{} -- {} views\n".format(author[0], author[1])
        print string2
        f.write(string2)
    f.write("\n")


def print_errors_over_one():
    """Prints out the days where more than 1%
    of logged access requests were errors."""
    query = '''
    SELECT date, percent
    FROM
        (SELECT date,
        (CAST(db_counts.bad AS float) * 100/ CAST(db_counts.total AS FLOAT))
        AS percent
        FROM
            (SELECT count(*) AS total,
            count(CASE WHEN status != '200 OK' THEN 'x' ELSE NULL END) AS bad,
            date(time) FROM log GROUP BY date(time)) AS db_counts)
            AS db_percent
    WHERE percent > 1
    '''
    results = execute_query(query)

    q = "3. On which days did more than 1% of requests lead to errors? \n"
    print q
    f.write(q)

    for date in results:
        string3 = "{0:%B %d, %Y} -- {1}% errors".format(date[0], date[1])
        print string3
        f.write(string3)
    f.write("\n")

if __name__ == '__main__':
    f = open(OUTPUT, 'w')
    print_top_articles()
    print_top_authors()
    print_errors_over_one()
    f.close()
