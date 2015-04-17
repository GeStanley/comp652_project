__author__ = 'geoffrey'

import numpy
import matplotlib.pyplot as plt
import scipy.stats as stats
from numpy.lib import recfunctions as rfn

if __name__ == '__main__':

    dt = numpy.dtype([('time_id', 'S32'), ('congestion', 'f8'), ('hour', 'i8')])

    array = numpy.loadtxt('hour.txt', dtype=dt, delimiter=',')


    for hour in range(0, 24):

        hour_array = array[array['hour'] == hour]
        differences = numpy.diff(hour_array['congestion'])

        numpy.savetxt('differences_hour_'+ str(hour) +'.txt', differences, fmt=['%4.2f'])


        plt.subplot(3, 8, hour+1)
        plt.hist(differences, 100, range=(-30, 30), normed=True)

        differences.sort()
        mean = numpy.mean(differences)
        std = numpy.std(differences)
        # kurtosis = stats.kurtosis(differences)

        # pdf = stats.norm.pdf(differences, mean, std, kurtosis)

        model = stats.norm.fit(differences)

        #print stats.norm.stats(differences, moments='mvsk')

        plt.plot(differences, stats.norm.pdf(differences))
        # plt.show()

    # plt.savefig('24_hour_difference_distributions.png')
    plt.show()