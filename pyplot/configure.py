#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
"""Module for the configuration of the pyplot script

"""
from __future__ import print_function, absolute_import

import argparse
import os.path
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
    add_root_parser.set_defaults(execute=add_root_dir)

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

    script_directories = common.SCRIPT_DIRECTORIES
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
        indent = '\t' * level
        unique = cls.get_modules(dirname)
        init_content = cls.tformatter.format(cls.template, lines=unique)
        with open(os.path.join(dirname, '__init__.py'), 'w') as init_file:
            init_file.write(init_content)
        directory = os.path.split(dirname)[1]
        print(indent + " {directory} ".format(directory=directory)
              .center(50, '='))
        print(indent + "Available scripts:")
        for name in unique:
            print(indent + '\t' + name)

    @classmethod
    def update(cls, args):
        """Iteratively updates all all available scripts for the subdirectories"""
        for script_dir in cls.script_directories:
            print('Updating ' + script_dir)
            for dirpath, _, _ in os.walk(script_dir):
                level = dirpath.replace(script_dir,'').count(os.sep)
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


def add_root_dir(args):
    """Add `dirname` to the config file as a script directory"""
    if not os.path.isdir(args.directory):
        print('The given directory does not exist!')
        print(args.directory)
        return
    dirname = os.path.abspath(args.directory)
    if dirname not in common.SCRIPT_DIRECTORIES:
        new_script_directories = common.SCRIPT_DIRECTORIES + [dirname,]
        common.CONFIG.setlist('include', 'script_directories', new_script_directories)
        with open(common.CONFIG_FILE, 'w') as config_fp:
            common.CONFIG.write(config_fp)


def main(args):
    args.execute(args)


if __name__ == '__main__':
    PARSER = get_parser()
    ARGS = PARSER.parse_args()
    main(ARGS)
