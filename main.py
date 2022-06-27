#!/usr/bin/env python
from scripts.message_utils import fatal_error, output_message
from scripts.cli_parser import args, parser

from datetime import date, datetime
import sys

def _check_modules():
    try:
        from psycopg2 import __libpq_version__
        from yaml import __version__
        from dotenv import __all__
    except ModuleNotFoundError as error:
        fatal_error("MODULE_MISSING", module=str(error).removeprefix("No module named "))

def _check_input_date(str_date: str) -> str:
    try:
        date_object = datetime.strptime(str_date, "%Y-%m-%d").date()

        if date_object > date.today():
           fatal_error("FUTURE_DATE", date=str_date)

        return str(date_object)

    except ValueError as error:
        error = str(error)

        if error.startswith("unconverted"):
            fatal_error("DAY_OFF_RANGE", date=str_date)
        else:
            fatal_error("INVALID_PATTERN", date=str_date, today=date.today())

    except Exception as error:
        fatal_error("DATE_UNKNOW", error=error.capitalize())


if __name__ == "__main__":
    if args.SHOULD_PRINT_HELP:
        parser.print_help()
        sys.exit()

    output_message("START", date=args.DATE)

    _check_modules()

    from dotenv import load_dotenv
    load_dotenv()

    from scripts.extractor import Extractor
    from scripts.importer import Importer
    target_date = _check_input_date(args.DATE)

    extractor = Extractor(target_date)
    importer = Importer(target_date)

    args.EXCTRACT_CSV and extractor.extract_csv()
    args.EXTRACT_DB and  extractor.extract_db()
    args.LOAD_TO_DB and importer.import_to_postgres()
    args.GEN_QUERY and  importer.generate_final_query()

    output_message("END")
