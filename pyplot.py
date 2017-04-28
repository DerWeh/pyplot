#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
"""Module to bundle plotting scripts

`activate-global-python-argcomplete` must be run to enable auto completion
TODO: update config module to handle config file"""


from pyplot import pyplot


if __name__ == '__main__':
    raise SystemExit(pyplot.ifmain_wrapper())
