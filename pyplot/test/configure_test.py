"""
Tests to check some functionality of `configure`
"""

# from os import path, pardir
# from sys import path as syspath

# # append root of project
# PATH = path.abspath(path.dirname(__file__))
# syspath.insert(0, path.join(PATH, pardir))

from .. import configure
from textwrap import dedent


def test_template():
    """test the template used to write the '__init__' file"""
    template = configure.Updater.template
    t_form = configure.TemplateFormatter()
    filled = t_form.format(template, lines=('foo', 'bar'))
    correct = dedent(
        """\
        __all__ = [
            'foo',
            'bar',
        ]"""
    )
    assert filled == correct
