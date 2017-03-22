#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
"""Module to bundle plotting scripts

`activate-global-python-argcomplete` must be run to enable auto completion
TODO: update config module to handle config file"""
from __future__ import absolute_import, print_function

import argparse
import ConfigParser as configparser
import os
import sys
from collections import defaultdict

import argcomplete
import configure


CONFIG_FILE = '.pyplot.cfg'


class ConfigParser(configparser.SafeConfigParser):
    """Subclass of `SafeConfigParser`, able to handle lists."""
    def getlist(self, section, option, raw=False, vars=None):
        """
        Get an option list, from a list of lines

        Every item is a none empty line, starting with leading whitespace which
        will be striped.
        """
        value = self.get(section, option, raw, vars)
        items = [item.strip() for item in value.splitlines() if item.strip()]
        return items

    def setlist(self, section, option, value):
        """Write a list to the config file in format readable by `getlist`."""
        seperator = '\n\t'
        value_str = seperator + seperator.join(value)
        self.set(section, option, value_str)


# def read_configuration(config_file):
#     """Read configuration file `config_file` to determine script directories.

#     Parameters
#     ----------
#     config_file : string
#         Path of the configuration file to be read.

#     Returns
#     -------
#     script_directories : list
#         List of the directories from which scripts should be included.

#     TODO: allow local `config` files to overwrite the master file.
#     """
#     config = ConfigParser()
#     with open(config_file, 'r') as config_fp:
#         config.readfp(config_fp)
#     script_directories = config.getlist('include', 'script_directories')
#     return script_directories


def register_scripts(subparsers, dirname, root_dir):
    """Registers all scripts in `__all__` if dirname is module"""
    path_tail = os.path.split(root_dir)[1]
    dirname = str(dirname[dirname.find(path_tail):])
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
    def __init__(self, parser, roots):
        """The dependent parser_dict is created.

        `parser` will be assigned as it's root.
        """
        super(SubparserDict, self).__init__()
        self.parser_dict = ParserDict(self)
        subparsers = parser.add_subparsers(
            title='subcommands',
            dest='used_subparser',
        )
        for root_dir in roots:
            self.parser_dict[root_dir] = parser
            self[root_dir] = subparsers

    def __missing__(self, key):
        self[key] = self.parser_dict[key].add_subparsers(
            title='subcommands',
            dest='used_subparser',
        )
        return self[key]


def get_parser(roots):
    """Return Argument Parser, providing available scripts"""
    parser = argparse.ArgumentParser()
    subparsers = SubparserDict(parser, (os.path.split(root)[1] for root in roots))
    for root_dir in roots:
        dir, root_module_str = os.path.split(root_dir)
        sys.path.insert(0, dir)
        try:
            module = __import__(root_module_str)
        except ImportError:
            pass  # module contains no init file, configure add must be run
        sys.path.remove(dir)
        for dirpath, _, _ in os.walk(root_dir):
            register_scripts(subparsers, dirpath, root_dir)

    register_parser(subparsers[os.path.split(roots[0])[1]], 'configure', configure)

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
    replace_argv = [args.name,] + args.arguments
    sys.argv = replace_argv
    args.main()


def main(args):
    args.run(args)

if __name__ == '__main__':
    config = ConfigParser()
    with open(CONFIG_FILE, 'r') as config_fp:
        config.readfp(config_fp)
    SCRIPT_DIRECTORIES = config.getlist('include', 'script_directories')
    PARSER = get_parser(SCRIPT_DIRECTORIES)
    ARGS = PARSER.parse_args()
    main(ARGS)
