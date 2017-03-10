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
    for module_str in plotter.__all__:
        print 'plotter', module_str
        module = __import__('.'.join(('plotter', module_str)), fromlist=module_str)
        print 'success'
        module_subparser[module_str] = subparsers.add_parser(
            module_str, parents=[module.get_parser(add_help=False)],
            help=module.__doc__.split('\n', 1)[0]
        )
    configure = subparsers.add_parser('configure', help='configure this script.')

    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_arguments()
    print
    from plotter.plotn import main
    main(args)
