"""Parsing arguments and running reader."""

import argparse
import sys

from rss_reader import __version__
from rss_reader import rss


def limit(value):
    """Conversion function for parse args.

    Check if limit argument has positive value.
    """
    value = int(value)
    if value <= 0:
        raise ValueError('Limit must have positive value.')
    return value


def parse_args(args):
    """Parse args from given list."""
    parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader.')
    parser.add_argument('source', metavar='source', type=str, help='RSS URL')
    parser.add_argument('--limit', type=limit, help='Limit news tops if this parameter provided')
    parser.add_argument('--json', action='store_true', help='Print result as JSON in stdout')
    parser.add_argument('--version', action='version', version='RSS Reader ' + __version__, help='Print version info')
    parser.add_argument('--verbose', action='store_true', help='Outputs verbose status messages')
    return parser.parse_args(args)


def run():
    try:
        args = parse_args(sys.argv[1:])
        rss.run_reader(args)
    except Exception as exc:
        print('Error:', exc)


if __name__ == '__main__':
    run()
