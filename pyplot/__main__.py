# PYTHON_ARGCOMPLETE_OK
"""entry point for the console script"""
from . import pyplot
from . import common


def main():
    parser = pyplot.get_parser(common.ROOT_DIRECTORIES, common.SUB_DIRECTORIES)
    args = parser.parse_args()
    return pyplot.main(args)
