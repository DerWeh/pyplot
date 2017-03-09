#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
"""Module to bundle plotting scripts

`activate-global-python-argcomplete` must be run to enable auto completion """

import argparse
import argcomplete
import plotter



def parse_arguments():
    """Argument Parser, providing available scripts"""
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(
        title = 'plotter',
        description = 'available plotting scripts'
    )
    import plotter.plotn
    test = subparsers.add_parser('plotn', parents=[plotter.plotn.parse_arguments()], help=plotter.plotn.__doc__.split('\n',1)[0])
    configure = subparsers.add_parser('configure', help='configure this script.')
    # parser.add_argument('--largetest')
    # parser.add_argument('program', choices=('test1', 'test2'))

    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_arguments()
