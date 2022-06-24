<img src="https://i.imgur.com/2Lkns1O.png" align="left" width="185px"/>

# Indicium Tech - Code Challenge

> Indicium code challenge 2021 for Software Developer focusing on data projects.

Challenge Instructions: [techindicium/code-challenge](https://github.com/techindicium/code-challenge)

<br>

## What does this pipeline do?

* Extracts data from CSV file and Postgres database tables;
* Import them to a new Postgres database;
* Generate a CSV file joining the tables **orders** and **order_details**.

## Prerequisites

* Python 3
* Docker-compose
* Psycopg2

## Setup

**1.** Install **psycopg2** on a venv or globally.
```sh
  pip install psycopg2
```

**2.** Initialize the Postgres databases.
```sh
   docker-compose up -d
```

## Usage

```lua
   main.py [-h] [-a] [-e] [-ecsv] [-edb] [-l] [-q] [-d DATE]

  Options:
    -a, --execute-all     Execute all pipeline's operations.
    -e, --extract-all     Exctract data from CSV and Databse.
    -ecsv, --extract-csv  Exctract data from CSV.
    -edb, --extract-db    Exctract data from Databse.
    -l, --load            Import the data to Postgres Database.
    -q, --query           Generate a query that shows the orders and its details.
    -d DATE, --date DATE  Define a date in format "YYYY-MM-DD" to the operations. Default: current date.
```
<br>

To run the complete pipeline:

```sh
   python main.py -a
```
<br>

To choose a date for the operations (year-month-day format):

```sh
   python main.py [-operation] -d YYYY-MM-DD
```

**Exemple:**
> Import the data into the database and generate the CSV with the query, targeting the date June 25, 2022:

```sh
   python main.py -l -q -d 2022-06-25
```
<br>

To get full usage info use:

```sh
   python main.py -h
```

---

### What I've learned with this project?

* It increased my experience with SQL.
* Taught me how to extract and load databases from/to CSV.
* Allowed me to develop a CLI in python.
* Exercised my ability to document code.
* Made me gain experience in error handling.
