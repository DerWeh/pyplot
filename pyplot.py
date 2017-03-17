#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
"""Module to bundle plotting scripts

`activate-global-python-argcomplete` must be run to enable auto completion """
from __future__ import absolute_import, print_function

import argparse
import os
from collections import defaultdict

import argcomplete
import configure

SCRIPT_DIR = 'plotter'


def register_scripts(subparsers, dirname, fnames):
    """Registers all scripts in `__all__` if dirname is module"""
    dirname = str(dirname[dirname.find(SCRIPT_DIR):])
    parent_module_str = dirname.replace(os.sep, '.')
    try:
        parent_module = __import__(parent_module_str,
                                   fromlist=parent_module_str)
    except ImportError:
        #directories which aren't a module are ignored
        return
    try:
        parent_module.__all__
    except AttributeError:
        return
    for module_str in parent_module.__all__:
        module = __import__(parent_module_str + '.' + module_str, fromlist=module_str)
        register_parser(subparsers[parent_module_str], module_str, module)


class ParserDict(defaultdict):
    """Dictionary of the parsers in the parser tree

    the connection is always parser -> sub_parser -> parser -> sub_parser
    This dictionary contains the parser elements, which need to be stored in a
    `.` notation (e.g. 'root.sub.subsub').
    It is in a cyclic dependency with subparser_dict and should not explicitly
    be used, to avoid infinite recursion.
    """
    def __init__(self, subparser_dict):
        super(ParserDict, self).__init__()
        self.subparsers = subparser_dict

    def __missing__(self, key):
        parent, _, title = key.rpartition('.')
        self[key] = self.subparsers[parent].add_parser(
            title,
            help="::access members of {0}".format(title)
        )
        return self[key]


class SubparserDict(defaultdict):
    """dictionary for the added subparsers

    If the key doesn't exist, a new sub_parser will be added. It is only to be
    used with a dot notation (e.g. 'root.sub.subsub').
    """
    def __init__(self, parser):
        """The dependent parser_dict is created.

        `parser` will be assigned as it's root.
        """
        super(SubparserDict, self).__init__()
        self.parser_dict = ParserDict(self)
        self.parser_dict[SCRIPT_DIR] = parser

    def __missing__(self, key):
        self[key] = self.parser_dict[key].add_subparsers(
            title='subcommands',
            dest='used_subparser',
        )
        return self[key]


def get_parser():
    """Return Argument Parser, providing available scripts"""
    parser = argparse.ArgumentParser()
    subparsers = SubparserDict(parser)
    os.path.walk(os.path.join(os.path.dirname(__file__), SCRIPT_DIR),
                 register_scripts, subparsers)

    register_parser(subparsers[SCRIPT_DIR], 'configure', configure)

    argcomplete.autocomplete(parser)
    return parser


def register_parser(subparsers, module_str, module):
    """Add a parser `module_str` to `subparsers`
    
    The main function of `module` will be assigned to the `run` argument if
    `module` has a `get_parser` function, else `substitute` will be assigned."""
    try:
        paren_parser = module.get_parser(add_help=False)
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
    else:
        module_subparser = subparsers.add_parser(
            module_str, parents=(paren_parser,),
            description=module.__doc__,
            help=module.__doc__.split('\n', 1)[0]
        )
        module_subparser.set_defaults(run=module.main)


def substitute(args):
    """replace `sys.argv` to launch a script without 'get_parser'"""
    import sys
    replace_argv = [args.name,] + args.arguments
    sys.argv = replace_argv
    args.main()


def main(args):
    args.run(args)

if __name__ == '__main__':
    PARSER = get_parser()
    ARGS = PARSER.parse_args()
    main(ARGS)
