"""second script to test for generalization"""
import argparse


def get_parser(add_help=True):
    parser = argparse.ArgumentParser(description=__doc__.split('\n',1)[0],add_help=add_help)
    parser.add_argument('-s', '--start', action='store', type=int, default=0,
                        help='the number of the first iteration to plot')
    return parser

def main(args):
    from matplotlib.pyplot import *
    from numpy import *

    start = args.start

    i = start
    U = atleast_2d(loadtxt("Usteps.dat"))
    x = range(0,len(U[0]))
    for line in U[start:]:
        plot(x,line, label = "{0}".format(i))
        i+=1
    legend()
    xlabel('label'), ylabel('potential')
    show()


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    main(args)
