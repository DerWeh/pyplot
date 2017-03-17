#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
"""Module for the configuration of the pyplot script

"""
from __future__ import print_function, absolute_import

import argparse
import os.path
from string import Formatter


def get_parser(add_help=True):
    parser = argparse.ArgumentParser(description=__doc__.split('\n', 1)[0],
                                     add_help=add_help)
    subparsers = parser.add_subparsers()
    update_parser = subparsers.add_parser(
        'update', help='Updates the list of scripts in plotter',)
    update_parser.set_defaults(execute=Updater.update)
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

    projectroot = os.path.abspath(os.path.dirname(__file__))
    script_dir = os.path.join(projectroot, 'plotter')
    sf = TemplateFormatter()

    template = dedent(
        """\
        __all__ = [
        {lines:repeat:    '{{item}}',
        }]"""
    )

    @classmethod
    def is_valid(cls, filename):
        """checks if `filename` is a python script

        Also checks that `filename` starts with '.' to avoid swaps and similar.
        """
        from os.path import isfile, join
        valid = (isfile(join(cls.script_dir, filename)) and
                 '.py' in filename and not filename.startswith('.'))
        return valid

    @classmethod
    def get_moduels(cls, dirname):
        """Return all valid names of scripts in `script_dir`"""
        content = os.listdir(dirname)
        scripts = [file.split('.py')[0] for file in content if cls.is_valid(file)]
        module_names = set(scripts) - set(("__init__",))
        return module_names

    @classmethod
    def update_dir(cls, dirname):
        """update the available plotting scripts"""
        print("called with " + dirname)
        unique = cls.get_moduels(dirname)
        init_content = cls.sf.format(cls.template, lines=unique)
        with open(os.path.join(dirname, '__init__.py'), 'w') as init_file:
            init_file.write(init_content)
        print("`{directory}` was successfully updated."
              .format(directory=dirname))
        print("The scripts:")
        for name in unique:
            print(name)
        print("should now be available.")

    @classmethod
    def update(cls):
        """Iteratively updates all all available scripts for the subdirectories"""
        print("I was called, proceeding with" + cls.script_dir)
        os.path.walk(cls.script_dir,
                     lambda args, dirname, fnames: cls.update_dir(dirname),
                     None)


def main(args):
    args.execute()


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    main(args)
