import sys
from os import get_terminal_size

from scripts.constants import messages, cc, tint_text

_terminal_size = get_terminal_size().columns
_pretty_line = ("=" * _terminal_size).center(_terminal_size)

def _print_pretty_msg(msg: str):
    msgs_list = [line.center(_terminal_size) for line in msg.split('\n')]
    print('\n' + _pretty_line)

    for msg in msgs_list:
        print(msg)

    print(_pretty_line)
    
class Printer:
    """A simple console printer."""
    
    @classmethod
    def fatal_error(self, *_id, **kwargs):
        """
        Print a message in console and exit.

        Parameters:
            `*_id`: str - the error ID.
            `**kwargs`: str | None - the args to format the message.
        """
        
        error = _id[0]
        msg = messages.ERRORS[error].format(**kwargs)
        
        print(tint_text("\n# Error: ", cc.RED) + msg)
        
        _print_pretty_msg("An error occurred, pipeline unfinished.")
        sys.exit(2)

    @classmethod
    def skip_operation(self, *_id, **kwargs):
        """
        Print a skip warning in console and return `False`.

        Parameters:
            `*_id`: str - the reason ID.
            `**kwargs`: str | None - the args to format the message.
        """

        reason = _id[0]

        msg = messages.SKIPS[reason].format(**kwargs)
        print(tint_text(f"\n\t#Skipping: ", cc.YELLOW) + msg)
        return False
    
    @classmethod
    def output_message(self, *_id, **kwargs):
        """
        Print a message in console.

        Parameters:
            `*_id`: str - the message ID.
            `**kwargs`: str | None - the args to format the message.
        """

        _id = _id[0]
        msg = messages.OUTPUTS[_id].format(**kwargs)

        if _id in ("START", "END"):
            _print_pretty_msg(msg)
            return

        mark = tint_text(">", cc.YELLOW)
        print(f"\n{mark} {msg}...")
    
    @classmethod
    def success(self) -> bool:
        """Print `"✔  Done!"` and return `True`"""
        print(tint_text("\n\t✔  Done!", cc.GREEN))
        return True