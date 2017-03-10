"""
Tests to check some functionality of `configure`
"""

from os import path, pardir
from sys import path as syspath

# append root of project
PATH = path.abspath(path.dirname(__file__))
syspath.append(path.join(PATH, pardir))

import pytest
from .. import configure
from textwrap import dedent


def test_template():
    template = configure.Updater.template
    sf = configure.TemplateFormatter()
    filled = sf.format(template, lines=('foo', 'bar'))
    correct = dedent(
        """\
        __all__ = [
            'foo',
            'bar',
        ]"""
    )
    assert filled == correct
