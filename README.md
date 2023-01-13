# Data Pipelines with Airflow

This repository serves as a submission for Udacity data engineer nanodegree.

## Project Introduction
A music streaming company, Sparkify, has decided that it is time to introduce more automation and monitoring to their data warehouse ETL pipelines and come to the conclusion that the best tool to achieve this is Apache Airflow.

## How to Run?

This section describes how to get use this repositrory.

**Database setup**
To run this project you will need connectivity to a postgreSQL database with below details.
```
dbname=studentdb
user=student
password=student
```

**Python environemnt setup**
```
pip install -r requirements.txt
```

**Initialize the database**
```
python create_tables.py
```

**Run the ETL pipeline**
```
python etl.py
```

## Project Structure
```
\data --> holds the sample data for the project
\create_tables.py --> script to create the database and tables
\etl.py --> script which runs the etl pipeline
\sql_queries.py --> contains SQL queries run throughout the project
\etl.ipynb --> jupyter notebook that includes experimenting for the etl.py script
\test.ipynb --> jupyter notebook that includes sanity tests for the database
```

## Database design

The goal of the project is to run efficient queries on song playing analytics which is mainly sotred in the songplays table (fact table).
One extreme would be to just have one table and include all the information about users, songs and artists in the same table.
However in order to be conservative with space this project normalizes the data into seperate songs, users and artists tables (dim tables).
This allows us to keep seperate lists (tables) of those entities and gets rid of a lot of data duplication.

Additionally we could build extra indexes on the tables depending on the kind of queries we want to run in the future.

The etl read the data from JSON files, applies light transformations and writes it inot the postgres DB.

## Example queries and results for song play analysis

Which are the top 10 locations from where the users are accesing the app from.
```
SELECT location, COUNT(*) FROM songplays GROUP BY location ORDER BY COUNT(*) DESC LIMIT 10;
```

Inspect the app activity by day of the week and hour of day. This can be visualised in a heatmap.
```
SELECT t.weekday, t.hour, COUNT(*) FROM songplays sp JOIN time t ON sp.start_time = t.start_time GROUP BY t.weekday, t.hour ORDER BY t.weekday, t.hour;
```


## (Bonus) Helper Commands for postgreSQL

**login to psql with {postgres} user**
```
# linux
sudo -u {postgres} psql

# windows
psql -U postgres
```

**PSQL commands**
```
\conninfo # connection info
\l # list all databases
\dt # list all relations
\du # list all users
CREATE USER <username> WITH PASSWORD '<password>';
CREATE DATABASE <name> WITH OWNER <username>;
GRANT ALL PRIVILEGES ON DATABASE db_name to user_name;
ALTER USER username CREATEDB; # grant user privilege to create dbs
```

**reinstall pgsql DB**
```
# linux
sudo yum remove postgresql11-server

sudo rm -rf  /var/lib/pgsql/11/data
sudo /usr/pgsql-11/bin/postgresql-11-setup initdb

sudo systemctl start postgresql-11
sudo systemctl enable postgresql-11

sudo systemctl restart postgresql-11 # restart service
```

