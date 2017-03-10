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
    module_subparser = {}
    # for module in plotter.__all__:
    #     from plotter import module
    #     module_subparser[module] = subparsers.add_parser(
    #         str(modul), parents=[module.get_parser(help=False)
        

    from plotter import plotn
    test = subparsers.add_parser('plotn', parents=[plotn.get_parser(help=False)],
                                 help=plotn.__doc__.split('\n',1)[0])
    configure = subparsers.add_parser('configure', help='configure this script.')

    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_arguments()
    from plotter.plotn import main
    main(args)
