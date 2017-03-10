"""
Tests to check some functionality of `pyplot`
"""

from os import path, pardir
from sys import path as syspath

# append root of project
PATH = path.abspath(path.dirname(__file__))
syspath.append(path.join(PATH, pardir))

import pytest

from .. import pyplot
from ..configure import Updater

@pytest.mark.parametrize("arguments", [Updater.get_moduels(), ['configure', None]])
def test_trivial(arguments, capsys):
    """runs the help messages"""
    for arg in arguments:
        parser = pyplot.get_parser()
        with pytest.raises(SystemExit):
            parser.parse_args([arg, '--help'])
    out, err = capsys.readouterr()
    assert 'usage: 'in out
