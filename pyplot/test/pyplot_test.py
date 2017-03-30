"""
Tests to check some functionality of `pyplot`

TODO: change the test to a test directory
"""
import pytest

from .. import pyplot
from ..configure import Updater


@pytest.mark.parametrize(
    "arguments",
    [Updater.get_modules(root_dir) for root_dir in Updater.root_directories] +
    [[(sub_dir, command) for command in Updater.get_modules(sub_dir)] for sub_dir in Updater.sub_directories] +
    [('configure', None),]
)
def test_trivial(arguments, capsys):
    """runs the help messages"""
    for arg in arguments:
        parser = pyplot.get_parser(pyplot.ROOT_DIRECTORIES, pyplot.SUB_DIRECTORIES)
        with pytest.raises(SystemExit):
            if isinstance(arg, tuple):
                parser.parse_args(arg + ('--help',))
            else:
                parser.parse_args([arg, '--help'])
    out, err = capsys.readouterr()
    assert 'usage: 'in out
