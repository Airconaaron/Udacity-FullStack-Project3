#!/usr/bin/env python2.7
# python file for specific SQL queries

import psycopg2

# connecting to database
db = psycopg2.connect("dbname=news")
f = open('output.txt', 'w')
c = db.cursor()

# 1. What are the most popular three articles of all time?

'''
This query first counts the number of successful http queries
and groups them together.
next we'll match them to the appropriate article titles from their slugs
and show only the top 3
'''
c.execute(
    '''
    select articles.title, log_new.views from
    articles join
    (select path, count(*) as views
    from log where (status = '200 OK') and
    path != '/' group by path) as log_new
    on log_new.path = concat('/article/', articles.slug)
    order by log_new.views desc
    limit 3
    '''
    )

q1 = c.fetchall()

# now print both to I/O and write to file.
print "Question 1:"
f.write("Question 1: \n")
for item in q1:
    print item
    f.write("{} -- {} views \n".format(item[0], item[1]))

# 2. Who are the most popular article authors of all time?
print "Question 2:"
f.write("Question2: \n")

'''
This query uses our previous query in a join statement.
It then connects each article to the author and sums up
their aggregate views.
'''
c.execute(
    '''
    select authors.name, sum(articles.views) from
    authors join (select articles.author, log_new.views from
    articles join (select path, count(*) as views
    from log where (status = '200 OK') and
    path != '/' group by path) as log_new
    on log_new.path = concat('/article/', articles.slug)
    order by log_new.views desc) as articles
    on authors.id = articles.author
    group by authors.id
    '''
    )
q2 = c.fetchall()

for author in q2:
    print author
    f.write("{} -- {} views\n".format(author[0], author[1]))

# 3. On which days did more than 1% of requests lead to errors?
print "Question 3:"
f.write("Question 3: \n")

c.execute(
    '''
    select date, percent from
    (select date, (db_counts.bad * 100/ db_counts.total) as percent,
    bad, total from (select count(*) as total,
    count(case when status != '200 OK' then 'x' else NULL end) as bad,
    date(time) from log group by date(time)) as db_counts) as db_percent
    where percent > 1
    '''
    )
q3 = c.fetchall()

for date in q3:
    print date
    f.write("{} -- {} errors".format(date[0], date[1]))

f.close()
db.close()
