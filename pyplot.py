#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
"""Module to bundle plotting scripts

`activate-global-python-argcomplete` must be run to enable auto completion """

import argparse
import argcomplete
import plotter
from configure import (get_parser as conf_get_parser,
                       main as conf_main)


def parse_arguments():
    """Argument Parser, providing available scripts"""
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(
        title='plotter',
        description= 'available plotting scripts',
        dest='used_subparser',
    )
    module_subparser = {}
    for module_str in plotter.__all__:
        module = __import__('plotter.' + module_str, fromlist=module_str)
        try:
            module_subparser[module_str] = subparsers.add_parser(
                module_str, parents=(module.get_parser(add_help=False),),
                description=module.__doc__,
                help=module.__doc__.split('\n', 1)[0]
            )
            module_subparser[module_str].set_defaults(run=module.main)
        except AttributeError:
            # module doesn't provide `get_parser`
            module_subparser[module_str] = subparsers.add_parser(
                module_str,
                description=module.__doc__,
                help=module.__doc__.split('\n', 1)[0],
            )
            module_subparser[module_str].add_argument(
                'arguments',
                nargs=argparse.REMAINDER,
                help='possible unknown arguments for {module}'.format(module=module_str),
            )
            module_subparser[module_str].set_defaults(run=substitute, name=module_str,
                                                      main=module.main)

    configure = subparsers.add_parser(
        'configure', parents=(conf_get_parser(add_help=False),),
        help='configure this script.'
    )
    configure.set_defaults(run=conf_main)

    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    return args


def substitute(args):
    import sys
    replace_argv = [args.name,] + args.arguments
    sys.argv = replace_argv
    args.main()


if __name__ == '__main__':
    args = parse_arguments()
    print args
    print "lets override sys.argv"
    args.run(args)
