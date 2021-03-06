#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
"""Module to bundle plotting scripts

`activate-global-python-argcomplete` must be run to enable auto completion
"""
from __future__ import absolute_import, print_function

import argparse
import os
import sys
from collections import defaultdict

import argcomplete
from . import __version__
from . import configure
from .common import ROOT_DIRECTORIES, SUB_DIRECTORIES


def register_scripts(subparsers, dirname, root_dir):
    """Registers all scripts in `__all__` if dirname is module"""
    path_tail = os.path.split(root_dir)[1]
    dirname = str(dirname[dirname.find(path_tail):])
    parent_module_str = dirname.replace(os.sep, '.')
    try:
        parent_module = __import__(parent_module_str,
                                   fromlist=parent_module_str)
    except ImportError:
        # directories which aren't a module are ignored
        return
    try:
        parent_module.__all__
    except AttributeError:
        return
    for module_str in parent_module.__all__:
        try:
            module = __import__(parent_module_str + '.' +
                                module_str, fromlist=module_str)
        except ImportError as imp_err:
            if 'no module' in str(imp_err).lower():
                print('Missing module '+module_str+'! Running `configure update` is required!',
                      file=sys.stderr)
            else:
                raise

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
        self.parser_dict['default'] = parser
        self['default'] = self.__missing__('default')

    def __missing__(self, key):
        self[key] = self.parser_dict[key].add_subparsers(
            title='subcommands',
            dest='used_subparser',
        )
        return self[key]

    def add_root(self, key):
        """Add *key* which refers to the root subparser *self['default']*"""
        self.parser_dict[key] = self.parser_dict['default']
        self[key] = self['default']

    def add_sub(self, key):
        """Add *key* which refers to a new parser of the root subparser"""
        self.parser_dict[key] = self['default'].add_parser(
            key,
            help="::access members of {0}".format(key)
        )
        self[key] = self.__missing__(key)


def get_parser(roots, subs):
    """Return Argument Parser, providing available scripts"""
    parser = argparse.ArgumentParser()
    subparsers = SubparserDict(parser)
    for adder, directories in ((subparsers.add_root, roots),
                               (subparsers.add_sub, subs)):
        for dir in directories:
            module_dir, module_str = os.path.split(dir)
            adder(module_str)
            sys.path.insert(0, module_dir)
            try:
                __import__(module_str)
            except ImportError:
                pass  # module contains no init file, configure add must be run
            sys.path.remove(module_dir)
            for dirpath, dirnames, _ in os.walk(dir, topdown=True):
                for directory in [_dir for _dir in dirnames if _dir.startswith('.')]:
                    dirnames.remove(directory)
                register_scripts(subparsers, dirpath, dir)
    register_parser(subparsers['default'], 'configure', configure)

    parser.add_argument('--version', action='version',
                        version='%(prog)s '+__version__)

    argcomplete.autocomplete(parser)
    return parser


def register_parser(subparsers, module_str, module):
    """Add a parser `module_str` to `subparsers`

    The main function of `module` will be assigned to the `run` argument if
    `module` has a `get_parser` function, else `substitute` will be assigned."""
    try:
        help_str = module.__doc__.split('\n', 1)[0]
    except AttributeError:
        help_str = ''
    try:
        paren_parser = module.get_parser(add_help=False)
    except AttributeError:
        # module doesn't provide `get_parser`
        module_subparser = subparsers.add_parser(
            module_str,
            description=module.__doc__,
            help=help_str
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
            help=help_str
        )
        module_subparser.set_defaults(run=module.main)


def substitute(args):
    """replace `sys.argv` to launch a script without 'get_parser'"""
    replace_argv = [args.name, ] + args.arguments
    sys.argv = replace_argv
    args.main()


def main(args):
    args.run(args)


def ifmain_wrapper():
    """Function bundling the calls in `ifmain` to reduce redundancy"""
    try:
        parser = get_parser(ROOT_DIRECTORIES, SUB_DIRECTORIES)
    except Exception as exc:
        # in case of an error try to directly launch configure script
        if sys.argv[1] == 'configure':
            print('Error occurred:', exc)
            print('Continue using `configure` directly')
            config_parser = configure.get_parser()
            config_args = config_parser.parse_args(sys.argv[2:])
            configure.main(config_args)
        else:
            raise
    else:
        args = parser.parse_args()
        main(args)


if __name__ == '__main__':
    ifmain_wrapper()
