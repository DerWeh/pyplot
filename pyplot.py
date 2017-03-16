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
from collections import defaultdict

SCRIPT_DIR = 'plotter'


# def _help(arg, dirname, fnames):
#     print((dirname.replace(os.sep, '.')))
#     return (dirname.replace(os.sep, '.'))

# os.path.walk('plotter', _help, None)
# def register_subparsers(subparsers, parser):
#     subparsers[name].add_subparsers(
#         title=str(parser)

#     )
class parser_dict(defaultdict):
    def __init__(self, subparser_dict):
        super(defaultdict, self).__init__()
        self.subparsers = subparser_dict

    def __missing__(self, key):
        parent, _, title = key.rpartition('.')
        self[key] = self.subparsers[parent].add_parser(
            title,
            help="access members of {0}".format(title)
        )
        return self[key]


class subparser_dict(defaultdict):
    """dictionary for the added subparsers

    if the key doesn't exist, a new sub_parser with the title of the key will
    be added"""
    def __init__(self, parser):
        super(defaultdict, self).__init__()
        # self.parser = parser
        self.parser_dict = parser_dict(self)
        self.parser_dict[SCRIPT_DIR] = parser

    def __missing__(self, key):
        print(key)
        print(key.rpartition('.')[0])
        # parent, _, title = key.rpartition('.')
        # if parent:
        #     self.parser_dict[parent] = self[parent].add_parser(
        #         title,
        #         help="access members of {0}".format(parent)
        #     )
        #     self[key] = self.parser_dict[parent].add_subparsers(
        #         title=key,
        #         dest='used_subparser',
        #     )
        # else:
        #     self[key] = self.parser.add_subparsers(
        #         title=key,
        #         dest='used_subparser',
        #     )
        self[key] = self.parser_dict[key].add_subparsers(
            title=key,
            dest='used_subparser',
        )
        return self[key]


def get_parser():
    """Return Argument Parser, providing available scripts"""
    parser = argparse.ArgumentParser()
    subparsers = subparser_dict(parser)
    for module_str in plotter.__all__:
        module = __import__(SCRIPT_DIR + '.' + module_str, fromlist=module_str)
        register_parser(subparsers[SCRIPT_DIR], module_str, module)

    module = __import__('plotter.sub1.toyplot', fromlist='toyplot')
    # sub1 = subparsers[SCRIPT_DIR].add_parser('sub1', help='this is my sub')
    # sub1_sub = sub1.add_subparsers(title='sub1_sub', dest='used_subparser')
    # register_parser(sub1_sub, 'toyplot', module)

    register_parser(subparsers['plotter.sub1'], 'toyplot', module)

    register_parser(subparsers[SCRIPT_DIR], 'configure', configure)

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
