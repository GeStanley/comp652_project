__author__ = 'geoffrey'

import numpy
import matplotlib.pyplot as plt

if __name__ == '__main__':
    dt = numpy.dtype([('error', 'f8')])

    array = numpy.loadtxt('outlier_error.txt', dtype=dt, delimiter=',')

    x = numpy.arange(0, 25)

    plt.plot(x, array[0:25])
    plt.xlabel('percent')
    plt.ylabel('mean squared error')
    plt.show()