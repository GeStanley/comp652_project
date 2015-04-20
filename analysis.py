__author__ = 'geoffrey'

import numpy
import scipy
import matplotlib.pyplot as plt
import scipy.stats as stats
from numpy.lib import recfunctions as rfn

def describe_data(x):
    n, min_max, mean, var, skew, kurt = scipy.stats.describe(x)
    print 'number of points: ', n
    print 'min/max: ', min_max
    print 'mean: ', mean
    print 'variance: ', var
    print 'skew: ', skew
    print 'kurtosis: ', kurt
    print 'median: ', scipy.median(x)


if __name__ == '__main__':

    dt = numpy.dtype([('time_id', 'S32'), ('congestion', 'f8'), ('hour', 'i8')])

    array = numpy.loadtxt('hour.txt', dtype=dt, delimiter=',')


    all_differences = numpy.diff(array['congestion'])

    plt.plot(all_differences)
    plt.ylabel("$\Delta $ \$")
    plt.xlabel("t")
    plt.show()


    for hour in range(0, 24):

        hour_array = array[array['hour'] == hour]
        differences = numpy.diff(hour_array['congestion'])

        #differences = numpy.hstack((stats.norm.rvs(-5, 2, 100), stats.norm.rvs(10, 1, 100)))

        describe_data(differences)

        numpy.savetxt('differences_hour_'+ str(hour) +'.txt', differences, fmt=['%4.2f'])

        plt.subplot(3, 8, hour+1)
        plt.hist(differences, 100, range=(-20, 20), normed=True)
        plt.xticks(numpy.arange(-20, 21, 10))
        plt.ylim(0, 0.5)

        differences.sort()
        # n = differences.size
        # percentile = round(n / 100, 0)
        # subset = differences[percentile : n - percentile]

        x = numpy.linspace(-20, 20, 100)

        #params = stats.norm.fit(differences)

        #pdf_fitted = stats.norm.pdf(x, loc=params[0], scale=params[1])

        pdf = stats.gaussian_kde(differences)

        plt.plot(x, pdf(x), 'g-')

    plt.show()


    # plt.savefig('24_hour_difference_distributions.png')
    # plt.show()