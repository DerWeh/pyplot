#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
"""Module to bundle plotting scripts

`activate-global-python-argcomplete` must be run to enable auto completion
TODO: update config module to handle config file"""

from pyplot import pyplot
from pyplot import common


if __name__ == '__main__':
    PARSER = pyplot.get_parser(common.SCRIPT_DIRECTORIES)
    ARGS = PARSER.parse_args()
    raise SystemExit(pyplot.main(ARGS))
