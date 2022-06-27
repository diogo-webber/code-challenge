import sys
from os import get_terminal_size, getenv

_can_handle_colours = getenv("TERM") or getenv("TERM_PROGRAM")

def colour(code):
    return f'\u001b[{code}m'

class cc():
    """Console Colours"""
    RED = colour('31')
    YELLOW = colour('33;1')
    GREEN = colour('38;5;40')
    RESET = colour('0')

def _tint(str, colour):
    return _can_handle_colours and colour + str + cc.RESET or str

def _tint_kwargs(kwargs, colour):
    for k, v in kwargs.items():
        v =  str(v) and v.replace("'", '')
        kwargs[k] = _tint('"'+ v +'"', colour)
    
    return kwargs
    
_Errors = {
    'DB_OFFLINE' : 'Could not connect to database {db_name}.\nIt looks like it is offline, use '+ _tint('"docker-compose up -d"', cc.RED) + ' to run it.',
    'DB_LOADING' : 'The database {db_name} is still starting, wait a few seconds and try again.',
    'DB_FAIL' : 'Could not connect to database {db_name}...\n\n * Exception:\n\n{error}',
    'MODULE_MISSING' :  'Required module {module} not found.',
    'DAY_OFF_RANGE' :  'Date provided {date} exceeds the number of days in the month.',
    'INVALID_PATTERN' :  'Date provided {date} does not match format ' +_tint('"YYYY-MM-DD"', cc.RED) + '.\n\nValid date example: {today}',
    'FUTURE_DATE' :  'Date provided {date} is in the future!',
    'DATE_UNKNOW' :  '{error}',
    'INVALID_YML_SERVICES' :  'It looks like you changed the name of the services in the file '+ _tint('"docker-compose.yml"', cc.RED)+', please revert them to '+_tint('"source_db"', cc.RED)+' and '+_tint('"output_db"', cc.RED)+'.',
}

_Skips = {
    'NO_SOURCE_CSV' : 'Could not find the CSV file in the default path: {path}\n\tSkipping CSV extraction...',
    'CSV_EXIST' : 'Data for date {date} already exists!\n\tSkipping CSV extraction...',
    'CSV_TABLES_EXIST' : 'Data for date {date} already exists!\n\tSkipping database extraction...',
    'IMPORT_NO_DATA' : 'There is no data/little available for import for the date {date}. You need to extract them first.',
    'QUERY_NO_DATA' : 'The orders or order_details tables are empty.\n\tYou must import the data first.',
}

_Msgs = {
    'START' : "Starting Pipeline Execution...\nTarget Date: {date}",
    'END' : "All operations finalized.",
    'CSV' : "Extrating CSV file",
    'DB' : "Extrating source database tables",
    'IMPORT' : "Loading CSV files into new database",
    'QUERY' : 'Exporting orders and orders_details tables to "{name}" file',
}

_terminal_size = get_terminal_size().columns
_pretty_line = ("=" * _terminal_size).center(_terminal_size)

def _pretty_msg(msg: str):
    msgs_list = [line.center(_terminal_size) for line in msg.split('\n')]
    print('\n' + _pretty_line)

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

    kwargs = _tint_kwargs(kwargs, cc.RED)

    msg = _Errors[error[0]].format(**kwargs)
    print(_tint("\n# Fatal Error: ", cc.RED) + msg)
    _pretty_msg("An error occurred, pipeline unfinished.")
    sys.exit(2)

def skip_operation(*reason, **kwargs):
    """
    Print a skip warning in console and return `False`.

    Parameters:
        `*reason`: str - the reason ID.
        `**kwargs`: str | None - the args to format the message.
    """
    
    kwargs = _tint_kwargs(kwargs, cc.YELLOW)

    msg = _Skips[reason[0]].format(**kwargs)
    print(_tint(f"\n\t# Warning: ", cc.YELLOW) + msg)
    return False

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

    mark = _tint(">", cc.YELLOW)
    print(f"\n{mark} {msg}...")

def sucess() -> bool:
    """Print `"Done!"` and return `True`"""
    print(_tint("\n\t✔  Done!", cc.GREEN))
    return True