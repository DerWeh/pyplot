#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
"""Module to bundle plotting scripts

`activate-global-python-argcomplete` must be run to enable auto completion """
from __future__ import absolute_import, print_function

import argparse
import argcomplete
import plotter
import os
import os.path
import configure

SCRIPT_DIR = 'plotter'


# def _help(arg, dirname, fnames):
#     print((dirname.replace(os.sep, '.')))
#     return (dirname.replace(os.sep, '.'))

# os.path.walk('plotter', _help, None)
# def register_subparsers(subparsers, parser):
#     subparsers[name].add_subparsers(
#         title=str(parser)
#     )


def get_parser():
    """Return Argument Parser, providing available scripts"""
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(
        title=SCRIPT_DIR,
        description='available plotting scripts',
        dest='used_subparser',
    )
    for module_str in plotter.__all__:
        module = __import__(SCRIPT_DIR + '.' + module_str, fromlist=module_str)
        register_parser(subparsers, module_str, module)

    register_parser(subparsers, 'configure', configure)

    argcomplete.autocomplete(parser)
    return parser


def register_parser(subparsers, module_str, module):
    """register `module` to `subparsers`"""
    try:
        module_subparser = subparsers.add_parser(
            module_str, parents=(module.get_parser(add_help=False),),
            description=module.__doc__,
            help=module.__doc__.split('\n', 1)[0]
        )
        module_subparser.set_defaults(run=module.main)
    except AttributeError:
        # module doesn't provide `get_parser`
        module_subparser = subparsers.add_parser(
            module_str,
            description=module.__doc__,
            help=module.__doc__.split('\n', 1)[0],
        )
        module_subparser.add_argument(
            'arguments',
            nargs=argparse.REMAINDER,
            help='possible unknown arguments for {module}'.format(module=module_str),
        )
        module_subparser.set_defaults(run=substitute, name=module_str, main=module.main)


def substitute(args):
    """replace `sys.argv` to launch a script without 'get_parser'"""
    import sys
    replace_argv = [args.name,] + args.arguments
    sys.argv = replace_argv
    args.main()


def main(args):
    args.run(args)

if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    main(args)
