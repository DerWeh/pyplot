"""Create a new tag as release.

This manually sets the version number to get it right."""
from __future__ import print_function

import argparse
import errno
import sys
import os
import subprocess


def substitute(*args):
    """Function to replace `subprocess.check_call` for testing.

    Only prints the arguments."""
    for arg in args:
        print(' '.join(arg))


version_file = os.path.join(os.path.dirname(__file__), 'pyplot', '__version__.py')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('version', type=str, help='The new version number')
    parser.add_argument('-d', '--dry_run', action='store_true',
                        help='print actions instead of executing them')
    args = parser.parse_args()
    if args.dry_run:
        subprocess.check_call = substitute
    if not valid_version(args.version):
        print(args.version + " is an invalid version number!\n"
              + "Please use a version of the form 'x.x.x' where `x` are integers.",
              file=sys.stderr)
        sys.exit(errno.EINVAL)
    for old_number, new_number in zip(old_version().split('.'), args.version.split('.')):
        if int(new_number) > int(old_number.split('-')[0]):
            break
    else:
        print("New version " + args.version + " is not bigger than the old version " + old_version(),
              file=sys.stderr)
        sys.exit(errno.EINVAL)
    write_version(args.version)
    subprocess.check_call(['git', 'tag', '-a ' + args.version, "-m 'Version " + args.version + "'"])
    if not args.dry_run:
        print('Sucessfully created new tag ' + args.version)


def valid_version(version):
    """Return true if the **version** has the format 'x.x.x' with integers `x`"""
    try:
        numbers = [int(part) for part in version.split('.')]
    except ValueError:
        return False
    if len(numbers) == 3:
        return True
    else:
        return False


def old_version():
    """Return the old version from the version file"""
    with open(version_file, 'r') as file_:
        for line in file_.readlines():
            if "__version__" in line:
                version = line.strip().split('=')[-1].strip(" '\"")
                break
        else:
            raise ValueError("Could not read or generate version")
    return version


def write_version(version):
    """Write the **version** to the file and commit it to *git*"""
    if subprocess.check_call is not substitute:
        with open(version_file, 'w') as file_:
            file_.writelines([
                '"""The package version"""\n',
                '# Do not change this file, it is automatically generated.\n'
                '__version__ = "' + version + '"',
            ])
    else:
        print("__version__".center(50, '*'))
        print('__version__ = "' + version + '"')
        print("".center(50, '*'))

    subprocess.check_call(['git', 'add', version_file])
    subprocess.check_call(['git', 'commit', "-m 'New version " + version + "'"])


if __name__ == '__main__':
    main()
