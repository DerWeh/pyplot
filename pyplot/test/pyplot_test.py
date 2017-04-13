"""
Tests to check some functionality of `pyplot`

TODO: change the test to a test directory
"""
import pytest

from os import path

from .. import pyplot
from ..configure import Updater

DIRECTORY = path.join(path.dirname(__file__), 'script_dir')


@pytest.mark.parametrize(
    "arguments",
    [Updater.get_modules(DIRECTORY)] +
    [('script_dir', command) for command in Updater.get_modules(DIRECTORY)] +
    [('configure', None), ]
)
def test_trivial(arguments, capsys):
    """runs the help messages"""
    for arg in arguments:
        parser = pyplot.get_parser([DIRECTORY, ], [DIRECTORY, ])
        with pytest.raises(SystemExit):
            if isinstance(arg, tuple):
                parser.parse_args(arg + ('--help',))
            else:
                parser.parse_args([arg, '--help'])
    out, err = capsys.readouterr()
    assert 'usage: 'in out
