# PYTHON_ARGCOMPLETE_OK
"""entry point for the console script"""
from .pyplot import ifmain_wrapper


def main():
    raise SystemExit(ifmain_wrapper())
