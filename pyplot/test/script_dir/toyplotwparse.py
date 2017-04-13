# PYTHON_ARGCOMPLETE_OK
"""toy script to test with."""
from __future__ import print_function

import argparse


def get_parser(add_help=True):
    parser = argparse.ArgumentParser(description=__doc__.split('\n',1)[0],add_help=add_help)
    parser.add_argument('-s', '--start', action='store', type=int, default=0,
                        help='the number of the first iteration to plot')
    return parser


def main(args):
    print("Just a toy example with the right structure which does nothing.")


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    main(args)
