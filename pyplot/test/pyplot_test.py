"""
Tests to check some functionality of `pyplot`
"""
import pytest

from .. import pyplot
from ..configure import Updater


@pytest.mark.parametrize("arguments", [Updater.get_modules(Updater.script_directories[0]),
                                       ['configure', None]])
def test_trivial(arguments, capsys):
    """runs the help messages"""
    for arg in arguments:
        parser = pyplot.get_parser(pyplot.SCRIPT_DIRECTORIES[0:1])
        with pytest.raises(SystemExit):
            parser.parse_args([arg, '--help'])
    out, err = capsys.readouterr()
    assert 'usage: 'in out
