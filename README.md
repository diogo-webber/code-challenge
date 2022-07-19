<img src="https://i.imgur.com/2Lkns1O.png" align="left" width="185px"/>

# Indicium Tech - Code Challenge

> Indicium code challenge 2021/2022 for Software Developer focusing on data projects.

Challenge Instructions: [techindicium/code-challenge](https://github.com/techindicium/code-challenge)

<br>

## What does this pipeline do?

* Extracts data from CSV file and Postgres database tables;
* Import them to a new Postgres database;
* Generate a CSV file joining the tables **orders** and **order_details**.
<br>

## Prerequisites

* Python >=3.9
* Docker-compose
<br>

## Setup

**1.** Install the dependencies.
```sh
  pip install -r requirements.txt
```
<br>

**2.** Initialize the **postgres** databases.
```sh
   docker-compose up -d
```

<br>

**3.** You can configure some things in the `.env` file.

<br>

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
> Load the data extracted into the new database and generate the CSV file with the query result, targeting the date June 25, 2022:

```sh
   python main.py -l -q -d 2022-06-25
```
<br>

To get full usage info use:

```sh
   python main.py -h
```

<br>

---

<br>

<details>
<summary><h2>Explaining/basing my decisions:<h2></summary>

<br>

> #### Why postgrees database?
> * Since the source database is on postgres, it's convenient use just one external library to manipulate them.<br>
> #### Why CSV format for the query result and extracted files?
> * Table type data is better represented in CSV files than in JSON or similar.<br>
> #### Why is the name of extract files in the format: <i>table_{table}_{date}</i>?
> * This format, with all the information, allows the file to be copied to another location while keeping all necessary information.<br>

</details>

<details>
<summary><h2>What I've learned with this project?<h2></summary>

   > * It increased my experience with SQL.
   > * Taught me how to extract and load databases from/to CSV.
   > * Allowed me to develop a CLI in python.
   > * Exercised my ability to document code.
   > * Made me gain experience in error handling.

</details>
