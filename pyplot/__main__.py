from . import pyplot
from . import common

def main():
    PARSER = pyplot.get_parser(common.SCRIPT_DIRECTORIES)
    ARGS = PARSER.parse_args()
    return pyplot.main(ARGS)
