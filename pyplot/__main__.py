# PYTHON_ARGCOMPLETE_OK
from . import pyplot
from . import common

def main():
    PARSER = pyplot.get_parser(common.ROOT_DIRECTORIES, common.SUB_DIRECTORIES)
    ARGS = PARSER.parse_args()
    return pyplot.main(ARGS)
