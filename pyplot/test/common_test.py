"""
Test to check some functionality of `common`
"""
try:
    from io import StringIO
except ImportError:
    from cStringIO import StringIO
from textwrap import dedent

import pytest

from .. import common

def test_configparser_getlist():
    """Test reading list with the common.ConfigParser."""
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
    """Test writing lists with the common.configparser."""
    config = common.ConfigParser()
    config.add_section('include')
    config.setlist('include', 'mylist', ('string1', 'string2', 'string3'))
    output = StringIO()
    config.write(output)
    output.seek(0)
    config.readfp(output)
    assert config.getlist('include', 'mylist') == ['string1', 'string2', 'string3']
