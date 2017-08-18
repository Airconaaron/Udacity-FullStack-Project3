# Udacity Project 3

This project is an exploration of SQL. The database here is a PostgreSQL database for a fictional news website.
The news database contains a articles, authors, and log table. 

The questions we thus want to answer using `python` and the `psycopg2` library are:
### 1. What are the most popular three articles of all time? 
### 2. Who are the most popular article authors of all time? 
### 3. On which days did more than 1% of requests lead to errors?

## Requirements
* Python2
* Vagrant
* VirtualBox

## Instructions
1. Install Vagrant and VirtualBox through [these steps](https://classroom.udacity.com/nanodegrees/nd004/parts/8d3e23e1-9ab6-47eb-b4f3-d5dc7ef27bf0/modules/bc51d967-cb21-46f4-90ea-caf73439dc59/lessons/5475ecd6-cfdb-4418-85a2-f2583074c08d/concepts/14c72fe3-e3fe-4959-9c4b-467cf5b7c3a0)
2. Next navigate to an appropriate directory and run `vagrant up` then `vagrant ssh` to start and then access our vm. 
3. Next download [this file](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) called `newsdata.sql` and place it in a file accessible to the vm.
4. To now setup the database run the command `psql -d news -f newsdata.sql`
Verify the installation by connecting to the database via `psql -d news` and running `\d`. You should see our authors, articles, and log tables. Run `\d TABLENAME` to see their specific schema. 
5. Finally to get the desired output run `python sql_queries.py`. This shoudl both print out the answers to the above questions and place them in a file called `output.txt`

