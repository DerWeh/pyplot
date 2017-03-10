#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
"""Module for the configuration of the pyplot script

"""
from __future__ import print_function

import argparse


def get_parser(add_help=True):
    parser = argparse.ArgumentParser(description=__doc__.split('\n',1)[0],
                                     add_help=add_help)
    subparsers = parser.add_subparsers()
    update_parser = subparsers.add_parser('update',
        help='Updates the list of scripts in plotter')
    update_parser.set_defaults(execute=update)
    return parser


def update():
    import os.path

    projectroot = os.path.abspath(os.path.dirname(__file__))
    script_dir = os.path.join(projectroot, 'plotter')
    content = os.listdir(script_dir)

    def is_valid(filename):
        # also check for leading '.' to ignore swaps etc.
        valid = (os.path.isfile(os.path.join(script_dir, filename)) and
                 '.py' in file and not filename.startswith('.'))
        return valid
    #TODO: clean this part up, it is to error prone without unit tests
    #TODO: use template for the file creation on keep readable script names

    scripts = ["'"+file.split('.py')[0]+"'," for file in content if is_valid(file)]
    unique = set(scripts) - set(("'__init__',",))

    template = """\
__all__ = [
{lines}
]
"""
    with open(os.path.join(script_dir, '__init__.py'), 'w') as init_file:
        init_file.write(template.format(lines='\n'.join(unique)))
    print("`plotter` was successfully updated.")
    print("The scripts:")
    for name in unique:
        print(name)
    print("should now be available.")


def main(args):
    args.execute()


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    main(args)
