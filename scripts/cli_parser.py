import argparse
from datetime import date
import sys

today_str = str(date.today())

parser = argparse.ArgumentParser(description='Extract and import data from/to Databases and CSV files.')
parser.version = '1.0'
parser.add_argument('-a', '--execute-all', action='store_true', help="Execute all pipeline's operations.")
parser.add_argument('-e', '--extract-all', action='store_true', help='Exctract data from CSV and Databse.')
parser.add_argument('-ecsv', '--extract-csv', action='store_true', help='Exctract data from CSV.')
parser.add_argument('-edb', '--extract-db', action='store_true', help='Exctract data from Databse.')
parser.add_argument('-l', '--load', action='store_true', help='Import the data to Postgres Database.')
parser.add_argument('-q', '--query', action='store_true', help='Generate a query that shows the orders and its details.')
parser.add_argument('-d', '--date', action='store', default=today_str,type=str, help='Define a date in format "YYYY-MM-DD" to the operations. Default: current date.')

raw_args = parser.parse_args()

class args():
    """Sanitized command line arguments."""
    SHOULD_PRINT_HELP: bool = len(sys.argv) == 1 or True not in dict(raw_args.__dict__).values()
    EXCTRACT_CSV: bool = raw_args.extract_csv or raw_args.extract_all or raw_args.execute_all
    EXTRACT_DB: bool = raw_args.extract_db or raw_args.extract_all or raw_args.execute_all
    LOAD_TO_DB: bool = raw_args.load or raw_args.execute_all
    GEN_QUERY: bool = raw_args.query or raw_args.execute_all
    DATE: str = raw_args.date
