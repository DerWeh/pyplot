#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
"""Module for the configuration of the pyplot script

"""
from __future__ import print_function, absolute_import, division

import argparse
import os.path
import sys
from string import Formatter
from functools import partial

from . import common


def get_parser(add_help=True):
    """Return the ArgumentParser, set add_help=False to use as parent."""
    parser = argparse.ArgumentParser(description=__doc__.split('\n', 1)[0],
                                     add_help=add_help)
    subparsers = parser.add_subparsers()
    update_parser = subparsers.add_parser(
        'update', help='Updates the list of scripts in plotter',)
    update_parser.set_defaults(execute=Updater.update)
    clean_parser = subparsers.add_parser(
        'clean', help='Removes all `__init__` files created by update')
    clean_parser.add_argument('-d', '--dryrun', action='store_true',
                              help='print files instead of deleting')
    clean_parser.set_defaults(execute=Updater.clean)
    add_root_parser = subparsers.add_parser(
        'addroot', help='Add new root_dir')
    add_root_parser.add_argument('directory')
    add_root_parser.set_defaults(execute=partial(add_directory, root=True))
    add_sub_parser = subparsers.add_parser(
        'addsub', help='Add new sub_dir')
    add_sub_parser.add_argument('directory')
    add_sub_parser.set_defaults(execute=add_directory)
    remove_parser = subparsers.add_parser(
        'rmdir', help='Removes directories form root and sub_dir list')
    remove_parser.set_defaults(execute=Remover.remove_directory)

    return parser


class TemplateFormatter(Formatter):
    """substitute formatter for easy template actions

    defines the following new formatter:
    `call`
        {foo} -> foo()
        the expression will be evaluated
    `repeat`
        {foo:repeat:bar {{item}}}
        the string after `repeat:` will be repeated for each item
    `if`
        {foo:if:bar}
        bar will be inserted if fo is True"""

    def format_field(self, value, spec):
        if spec == 'call':
            return value()
        elif spec.startswith('repeat'):
            template = spec.partition(':')[-1]
            if isinstance(value, dict):
                value = value.items()
            return ''.join((template.format(item=item) for item in value))
        elif spec.startswith('if'):
            return value and spec.partition(':')[-1]
        else:
            return super(TemplateFormatter, self).format_field(value, spec)


class Updater(object):
    """handles which plotting scripts are available"""
    from textwrap import dedent

    script_directories = set(common.ROOT_DIRECTORIES + common.SUB_DIRECTORIES)
    tformatter = TemplateFormatter()

    template = dedent(
        """\
        __all__ = [
        {lines:repeat:    '{{item}}',
        }]"""
    )

    @classmethod
    def is_valid(cls, filename, dirname):
        """checks if `filename` is a python script

        Filenames starting with `.` will be ignored (swaps and similar).
        """
        # Todo: import module to check if it has main method
        from os.path import isfile, join
        valid = (isfile(join(dirname, filename)) and
                 '.py' in filename and not filename.startswith('.'))
        return valid

    @classmethod
    def get_modules(cls, dirname):
        """Return all valid names of scripts in `dirname`"""
        content = os.listdir(dirname)
        scripts = [script.split('.py')[0] for script in content if
                   cls.is_valid(script, dirname)]
        module_names = set(scripts) - set(("__init__",))
        return module_names

    @classmethod
    def update_dir(cls, dirname, level=0):
        """update the available plotting scripts"""
        indent = '│   '*level + '├──'  # if level else ''
        unique = cls.get_modules(dirname)
        init_content = cls.tformatter.format(cls.template, lines=unique)
        with open(os.path.join(dirname, '__init__.py'), 'w') as init_file:
            init_file.write(init_content)
        for name in unique:
            print(indent + str(name))

    @classmethod
    def update(cls, args):
        """Iteratively updates all all available scripts for the subdirectories"""
        print('Updating')
        print('Available scripts:')
        print('-' * 50)
        for script_dir in cls.script_directories:
            print('├──<' + str(os.path.basename(script_dir)) +
                  '>    ' + str(script_dir))
            for dirpath, dirnames, _ in os.walk(script_dir, topdown=True):
                for directory in [_dir for _dir in dirnames if _dir.startswith('.')]:
                    dirnames.remove(directory)
                level = dirpath.replace(script_dir, '').count(os.sep) + 1
                cls.update_dir(dirpath, level)

    @classmethod
    def clean(cls, args):
        """remove all the `__init__` files in the subdirectories."""
        def _remove(pattern, dirname, fnames, dryrun=True):
            full_fnames = (os.path.join(dirname, fname) for fname in fnames
                           if pattern in fname)
            if dryrun:
                print('In directory ' + dirname)
                print('The following files will be removed: ')
                for name in full_fnames:
                    print('\t'+os.path.basename(name)+'\tfull name:'+name)
                print('--------------------------------------------------')
            else:
                for name in full_fnames:
                    os.remove(name)
                print(dirname+' cleaned.')
        for script_dir in cls.script_directories:
            for dirpath, _, fnames in os.walk(script_dir):
                _remove('__init__.py', dirpath, fnames, args.dryrun)


def add_directory(args, root=False):
    """Add `dirname` to the config file.

    If *root* is true it is added as root directory
    """
    if root:
        existing_dirs = common.ROOT_DIRECTORIES
        option = 'root_directories'
    else:
        existing_dirs = common.SUB_DIRECTORIES
        option = 'sub_directories'
    if not os.path.isdir(args.directory):
        print('The given directory does not exist!')
        print(args.directory)
        return
    dirname = os.path.abspath(args.directory)
    try:  # ensure that the section exits
        common.CONFIG.add_section('include')
    except common.configparser.DuplicateSectionError:
        pass
    if dirname not in existing_dirs:
        new_directories = existing_dirs + [dirname, ]
        common.CONFIG.setlist('include', option, new_directories)
        with open(common.CONFIG_FILE, 'w') as config_fp:
            common.CONFIG.write(config_fp)


class Remover(object):
    """Class to bundle functionality to remove directories from config"""
    directories = common.ROOT_DIRECTORIES + common.SUB_DIRECTORIES

    @classmethod
    def remove_directory(cls, args):
        """Dialog to remove directories from the configuration file"""
        cls.print_directory_list()
        root_length = len(common.ROOT_DIRECTORIES)
        index_dict = {index: (directory, common.ROOT_DIRECTORIES)
                      for index, directory in enumerate(common.ROOT_DIRECTORIES)}
        index_dict.update(
            {index+root_length: (directory, common.SUB_DIRECTORIES)
             for index, directory in enumerate(common.SUB_DIRECTORIES)}
        )
        while True:  # sys.exit will be called in process_input
            try:
                user_input = raw_input('>>> ')
            except NameError:
                user_input = input('>>> ')
            for item in user_input.split():
                cls.process_input(item, index_dict)

    @classmethod
    def print_directory_list(cls):
        """Prints the directories from the configuration file"""
        maxwidth = len(cls.directories)//10 + 1
        i = 0
        print("Root directories:")
        print("-" * 50)
        template_str = "{index:{width}} {directory}"
        for directory in common.ROOT_DIRECTORIES:
            print(template_str.format(index=i, width=maxwidth, directory=directory))
            i += 1
        print("Sub directories:")
        print("-" * 50)
        for directory in common.SUB_DIRECTORIES:
            print(template_str.format(index=i, width=maxwidth, directory=directory))
            i += 1
        print("-" * 50)
        print('Input number of directories not to handle anymore.')
        print("Save new configuration: ['q'], abort and discard: ['a']")

    @classmethod
    def process_input(cls, item, index_dict):
        """Handle a word of the user_input"""
        if item.lower() == 'q':
            common.CONFIG.setlist('include', 'root_directories', common.ROOT_DIRECTORIES)
            common.CONFIG.setlist('include', 'sub_directories', common.SUB_DIRECTORIES)
            with open(common.CONFIG_FILE, 'w') as config_fp:
                common.CONFIG.write(config_fp)
            print('Configuration file successfully updated.')
            sys.exit(0)
        elif item.lower() == 'a':
            print("Aborted, changes won't be saved")
            sys.exit(0)
        else:
            try:
                index = int(item)
            except ValueError:
                print('Invalid user input '+item, file=sys.stderr)
                sys.exit(1)
            directory, dir_list = index_dict.pop(index)
            dir_list.remove(directory)
            print(directory + ' removed')


def main(args):
    args.execute(args)


if __name__ == '__main__':
    PARSER = get_parser()
    ARGS = PARSER.parse_args()
    main(ARGS)
