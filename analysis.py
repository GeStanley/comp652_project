__author__ = 'geoffrey'

import numpy
import matplotlib.pyplot as plt
from numpy.lib import recfunctions as rfn

if __name__ == '__main__':

    dt = numpy.dtype([('time_id', 'S32'), ('congestion', 'f8'), ('hour', 'i8')])

    array = numpy.loadtxt('hour.txt', dtype=dt, delimiter=',')


    for hour in range(0, 24):
        print hour
        hour_array = array[array['hour'] == hour]
        differences = numpy.diff(hour_array['congestion'])

        print type(differences)

        #plt.hist(differences, 100, range=(-30, 30))

        #plt.show()