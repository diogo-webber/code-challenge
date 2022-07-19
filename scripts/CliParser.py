import argparse
from datetime import date
import sys

_today_str = str(date.today())

class _Args():
    def __init__(self, raw) -> None:
        self.SHOULD_PRINT_USAGE: bool = len(sys.argv) == 1 or (True not in dict(raw.__dict__).values())
        self.EXCTRACT_CSV: bool = raw.extract_csv or raw.extract_all or raw.execute_all
        self.EXTRACT_DB: bool = raw.extract_db or raw.extract_all or raw.execute_all
        self.LOAD_TO_DB: bool = raw.load or raw.execute_all
        self.GEN_QUERY: bool = raw.query or raw.execute_all
        self.DATE: str = raw.date

def _construct_parser():
    parser = argparse.ArgumentParser(description='Extract and import data from/to Databases and CSV files.')
    parser.version = '1.0'
    parser.add_argument('-a', '--execute-all', action='store_true', help="Execute all pipeline's operations.")
    parser.add_argument('-e', '--extract-all', action='store_true', help='Exctract data from CSV and Databse.')
    parser.add_argument('-ecsv', '--extract-csv', action='store_true', help='Exctract data from CSV.')
    parser.add_argument('-edb', '--extract-db', action='store_true', help='Exctract data from Databse.')
    parser.add_argument('-l', '--load', action='store_true', help='Import the data to Postgres Database.')
    parser.add_argument('-q', '--query', action='store_true', help='Generate a query that shows the orders and its details.')
    parser.add_argument('-d', '--date', action='store', default=_today_str, type=str, help='Define a date in format "YYYY-MM-DD" to the operations. Default: current date.')

    return parser

class CliParser():
    """Parse and sanitize command line arguments."""
    def __init__(self) -> None:
        self._parser = _construct_parser()
        raw_args = self._parser.parse_args()
        self.args = _Args(raw_args)
    
    def print_usage(self):
        self._parser.print_usage()