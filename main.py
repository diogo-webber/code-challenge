#!/usr/bin/env python

from scripts.Printer import Printer
from scripts.CliParser import CliParser

from datetime import date, datetime
import sys

def check_modules():
    """Check if all required modules are present."""
    try:
        from psycopg2 import __libpq_version__
        from yaml import __version__
        from dotenv import __all__
    except ModuleNotFoundError as error:
        Printer.fatal_error("MODULE_MISSING", module=str(error).removeprefix("No module named "))

def check_input_date(str_date: str) -> str:
    """Check if the date provided is valid."""
    try:
        date_object = datetime.strptime(str_date, "%Y-%m-%d").date()

        if date_object > date.today():
           Printer.fatal_error("FUTURE_DATE", date=str_date)

        return str(date_object)

    except ValueError as error:
        error = str(error)

        if error.startswith("unconverted"):
            Printer.fatal_error("DAY_OFF_RANGE", date=str_date)
        else:
            Printer.fatal_error("INVALID_PATTERN", date=str_date, today=date.today())

    except Exception as error:
        Printer.fatal_error("DATE_UNKNOW", error=error.capitalize())

def main(cli):
    args = cli.args
    
    if args.SHOULD_PRINT_USAGE:
        cli.print_usage()
        sys.exit(1)

    Printer.output_message("START", date=args.DATE)

    target_date = check_input_date(args.DATE)
    
    check_modules()

    from dotenv import load_dotenv
    load_dotenv()

    from scripts.Extractor import Extractor
    from scripts.Importer import Importer
    from scripts.DBCredentials import DBCredentials
    from scripts.Database import Database

    extractor = Extractor(target_date)
    importer = Importer(target_date)

    args.EXCTRACT_CSV and extractor.extract_csv()
    
    needs_source_db = args.EXTRACT_DB
    needs_output_db = args.LOAD_TO_DB or args.GEN_QUERY 
    
    if needs_source_db:
        source_db_credentials = DBCredentials(yml_service="source_db")
        source_db = Database(source_db_credentials)
        
        extractor.set_db(source_db)
    
    if needs_output_db:
        output_db_credentials = DBCredentials(yml_service="output_db")
        output_db = Database(output_db_credentials)
        
        importer.set_db(output_db)

    args.EXTRACT_DB and extractor.extract_db()
    args.LOAD_TO_DB and importer.import_to_postgres()
    args.GEN_QUERY  and importer.generate_final_query()
    
    needs_source_db and source_db.close_connection()
    needs_output_db and output_db.close_connection()

    Printer.output_message("END")
    
if __name__ == "__main__":
    main(CliParser())
