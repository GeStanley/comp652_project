__author__ = 'geoffrey'

import numpy
import scipy
import matplotlib.pyplot as plt
import scipy.stats as stats

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


    for hour in range(0, 2):

        hour_array = array[array['hour'] == hour]
        differences = numpy.diff(hour_array['congestion'])

        describe_data(differences)
        print ''

        pdf = stats.gaussian_kde(differences)

        x = numpy.linspace(-50, 50, 100)
        plt.plot(x, pdf(x), 'g-')
        plt.show()