"""existing plotting script to test with."""
import argparse

def parse_arguments():
    print __doc__
    parser = argparse.ArgumentParser(description=__doc__.split('\n',1)[0],add_help=False)
    parser.add_argument('-s', '--start', action='store', type=int, default=0,
                        help='the number of the first iteration to plot')
    return parser


def main(args):
    import pylab

    import numpy as np
    import matplotlib.pyplot as plt

    # parser = parse_arguments()
    # start = parser.parse_args().start
    start = args.start

    try:
        n = np.atleast_2d(np.loadtxt("nsteps.dat"))
    except IOError:
        n = np.atleast_2d(np.loadtxt("loop/nsteps.dat"))
    i = start
    x = range(0,len(n[0]))
    for line in n[start:]:
        plt.plot(x,line, label = "{0}".format(i))
        i+=1
    plt.legend()
    plt.xlabel('label'), plt.ylabel('occupation')

    param = None
    try:
        param = open('layer_hb_param.init', 'r')
        content = param.readlines()
    except IOError:
        try:
            param = open('../layer_hb_param.init', 'r')
            content = param.readlines()
        except IOError:
            pass
    finally:
        param.close()

    if param:
        N = int(content[5])
        U = np.fromstring(content[28 + N*2], sep = ' ')
        mu = np.fromstring(content[29 + N*2], sep = ' ')

        if(N>10):
            N = N/10
        else:
            N = 1
        pos = range(0,len(n[0]),N)
        labels = ['{0}\nU={1}\nmu={2}'.format(i,U[i],mu[i]) for i in pos]
        pylab.xticks(pos, labels)


    plt.show()


if __name__ == '__main__':
    parser = parse_arguments()
    args = parser.parse_args()
    main(args)
