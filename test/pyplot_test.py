"""
Tests to check some functionality of `pyplot`
"""

from os import path, pardir
from sys import path as syspath

# append root of project
PATH = path.abspath(path.dirname(__file__))
syspath.append(path.join(PATH, pardir))

import pytest
from cStringIO import StringIO
from textwrap import dedent

from .. import pyplot
from ..configure import Updater


@pytest.mark.parametrize("arguments", [Updater.get_modules(Updater.script_dir),
                                       ['configure', None]])
def test_trivial(arguments, capsys):
    """runs the help messages"""
    for arg in arguments:
        parser = pyplot.get_parser()
        with pytest.raises(SystemExit):
            parser.parse_args([arg, '--help'])
    out, err = capsys.readouterr()
    assert 'usage: 'in out


def test_configparser_getlist():
    config = pyplot.ConfigParser()
    test_list = dedent(
        """\
        [include]
        mylist =
            string1
            string2
            string3
        """
    )
    StringIO(test_list)
    config.readfp(StringIO(test_list))
    assert config.getlist('include', 'mylist') == ['string1', 'string2', 'string3']


def test_configparser_setlist():
    config = pyplot.ConfigParser()
    config.add_section('include')
    config.setlist('include', 'mylist', ('string1', 'string2', 'string3'))
    output = StringIO()
    config.write(output)
    output.seek(0)
    config.readfp(output)
    assert config.getlist('include', 'mylist') == ['string1', 'string2', 'string3']
