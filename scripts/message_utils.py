import sys
from os import get_terminal_size

_Errors = {
    'DB_CONNECT' : 'Could not connect to database "{db_name}". Is it up?\n\nThis is the exception:\n\n{error}',
    'PSYCOPG2_MISSING' :  'Required module "pyscopg2" not found.',
    'DAY_OFF_RANGE' :  'Date provided "{date}" exceeds the number of days in the month.',
    'INVALID_PATTERN' :  'Date provided "{date}" does not match format "YYYY-MM-DD".\n\nValid date example: {today}"',
    'FUTURE_DATE' :  'Date provided "{date}" is in the future!',
    'DATE_UNKNOW' :  '{error}',
}

_Skips = {
    'NO_SOURCE_CSV' : 'Could not find the CSV file in the default path: "{path}"\n\tSkipping CSV extraction...',
    'CSV_EXIST' : 'Data for date "{date}" already exists!\n\tSkipping CSV extraction...',
    'CSV_TABLES_EXIST' : 'Data for date "{date}" already exists!\n\tSkipping database extraction...',
    'QUERY_NO_DATA' : 'The orders and order_details tables are empty, you must import the database first.',
}

_Msgs = {
    'START' : "Starting Pipeline Execution...\nTarget Date: {date}",
    'END' : "All operations finalized.",
    'CSV' : "Extrating CSV file",
    'DB' : "Extrating Database Tables",
    'IMPORT' : "Loading CSV files into new Database",
    'QUERY' : 'Exporting orders and orders_details tables to "{name}.csv" file',
}

_terminal_size = get_terminal_size().columns
_pretty_line = ("=" * _terminal_size).center(_terminal_size)

def _pretty_msg(msg: str):
    msgs_list = [line.center(_terminal_size) for line in msg.split('\n')]

    print("\n" + _pretty_line)

    for msg in msgs_list:
        print(msg)

    print(_pretty_line)

def fatal_error(*error, **kwargs):
    """
    Print a message in console and exit.

    Parameters:
        `*error`: str - the error ID.
        `**kwargs`: str | None - the args to format the message.
    """

    msg = _Errors[error[0]].format(**kwargs)
    print(f"\n- Fatal Error: " + msg)
    _pretty_msg("An error occurred, pipeline unfinished.")
    sys.exit(2)

def skip_operation(*reason, **kwargs):
    """
    Print a skip warning in console.

    Parameters:
        `*reason`: str - the reason ID.
        `**kwargs`: str | None - the args to format the message.
    """

    msg = _Skips[reason[0]].format(**kwargs)
    print(f"\n\t# " + msg)

def output_message(*_id, **kwargs):
    """
     Print a message in console.

    Parameters:
        `*_id`: str - the message ID.
        `**kwargs`: str | None - the args to format the message.
    """

    msg =_Msgs[_id[0]]
    msg = msg.format(**kwargs)

    if _id[0] in ("START", "END"):
        _pretty_msg(msg)
        return

    print(f"\n> {msg}...")

def sucess() -> bool:
    """Print `"Done!"` and return `True`"""
    print("\n\tDone!")
    return True