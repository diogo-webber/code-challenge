
POSTGRES_FOLDER_PATTERN = "./data/postgres/{table}/{date}"
CSV_FOLDER_PATTERN = "./data/csv/{date}"

OUTPUT_FILE_NAME_PATTERN = "table_{table}_{date}.csv"

class SQL:
    """All SQL queries used in this pipeline."""
    LIST_TABLES = """
        SELECT tablename
        FROM pg_catalog.pg_tables
        WHERE schemaname NOT IN 
        ('information_schema', 'pg_catalog')
    """

    TRUNCATE_ALL = "TRUNCATE {select} CASCADE;"

    GENERIC_COPY_TO = """
        COPY ({select})
        TO STDOUT
        WITH HEADER CSV
        DELIMITER '|'
    """

    EXPORT_TO_CSV = GENERIC_COPY_TO.format(select="SELECT * FROM {table_name}")

    IMPORT_TO_DB = """
        COPY {table_name}
        FROM STDIN
        WITH HEADER CSV
        DELIMITER '|'
        NULL ''
    """

    SELECT_FINAL_QUERY = """
        SELECT * 
            FROM
                orders AS ord 
                INNER JOIN order_details AS dtl
                ON (ord.order_id = dtl.order_id)
    """

    FINAL_QUERY = GENERIC_COPY_TO.format(select=SELECT_FINAL_QUERY)
    
class messages:
    ERRORS = {
        'DB_OFFLINE' : 'Could not connect to database "{db_name}".\nIt looks like it\'s offline, use "docker-compose up -d" to run it.',
        'DB_LOADING' : 'The database "{db_name}" is still starting, wait a few seconds and try again.',
        'DB_FAIL' : 'Could not connect to database "{db_name}"...\n\n * Exception:\n\n{error}',
        'MODULE_MISSING' :  'Required module {module} not found.',
        'DAY_OFF_RANGE' :  'Date provided {date} exceeds the number of days in the month.',
        'INVALID_PATTERN' :  'Date provided {date} does not match format "YYYY-MM-DD".\n\nValid date example: {today}',
        'FUTURE_DATE' :  'Date provided {date} is in the future!',
        'DATE_UNKNOW' :  '{error}',
        'INVALID_YML_SERVICES' :  'It looks like you changed the name of the services in the "docker-compose.yml" file, please revert them to "source_db" and "output_db".',
    }

    SKIPS = {
        'NO_SOURCE_CSV' : 'Could not find the CSV file in the default path: {path}.',
        'CSV_EXIST' : 'Data for date {date} already exists!',
        'CSV_TABLES_EXIST' : 'Data for date {date} already exists!',
        'IMPORT_NO_DATA' : 'There is little or no data available for import for the date {date}. You need to extract them first.',
        'QUERY_NO_DATA' : 'The orders or order_details tables are empty.\n\tYou must import the data first.',
    }

    OUTPUTS = {
        'START' : "Starting Pipeline Execution...\nTarget Date: {date}",
        'END' : "All operations finalized.",
        'CSV' : "Extrating CSV file",
        'DB' : "Extrating source database tables",
        'IMPORT' : "Loading CSV files into new database",
        'QUERY' : 'Exporting "orders" and "orders_details" tables to "{name}" file',
    }

# -------------------------------------------------------------------- #

import re, os

def _colour(code):
    return f'\u001b[{code}m'

_can_handle_colours = os.getenv("TERM") or os.getenv("TERM_PROGRAM")

# -------------------------------------------------------------------- #

# Used by Printer.py
class cc:
    """Console Colours"""
    RED = _colour('31')
    YELLOW = _colour('33;1')
    GREEN = _colour('38;5;40')
    RESET = _colour('0')

# Used by Printer.py
def tint_text(str, colour: cc):
    return (_can_handle_colours and colour + str + cc.RESET) or str

# -------------------------------------------------------------------- #

def _tint_sub(colour):
    return lambda match: tint_text(match.group(0), colour)

def _tint_msg(msg: str, colour_fn, only_quoted: bool):
    quoted = re.sub('"(.*?)"', colour_fn, msg, re.M) # Color all quoted strings.
    if only_quoted: return quoted
    return re.sub('{(.*?)}', colour_fn, quoted, re.M) # Color all special parameters.

def _tint_msgs_dict(group: str, colour, only_quoted: bool=None):
    for key, msg in group.items():
        group[key] = _tint_msg(msg, _tint_sub(colour), only_quoted)

_tint_msgs_dict(messages.ERRORS, cc.RED)
_tint_msgs_dict(messages.SKIPS, cc.YELLOW)
_tint_msgs_dict(messages.OUTPUTS, cc.YELLOW, True)
