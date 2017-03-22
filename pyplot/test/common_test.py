"""
Test to check some functionality of `common`
"""
import pytest
from cStringIO import StringIO
from textwrap import dedent

from .. import common


def test_configparser_getlist():
    config = common.ConfigParser()
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
    config = common.ConfigParser()
    config.add_section('include')
    config.setlist('include', 'mylist', ('string1', 'string2', 'string3'))
    output = StringIO()
    config.write(output)
    output.seek(0)
    config.readfp(output)
    assert config.getlist('include', 'mylist') == ['string1', 'string2', 'string3']

