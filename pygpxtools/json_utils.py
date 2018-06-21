import json
from pygments import highlight, lexers, formatters


def json_formatter(data, colorize):
    """JSON output formatter

    Args:
        data (json): json output to pretty print
        colorize (bool): colorize or not output
    """

    if data != {}:
        output = json.dumps(data, indent=4, sort_keys=True, ensure_ascii=False)
        if colorize:
            print(highlight(output, lexers.JsonLexer(), formatters.TerminalFormatter()))
        else:
            print(output)