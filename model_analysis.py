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


    iterations = 10

    dt = numpy.dtype([('time_id', 'S32'), ('congestion', 'f8'), ('hour', 'i8')])

    array = numpy.loadtxt('hour.txt', dtype=dt, delimiter=',')


    for model_range in range(30, 31):

        for hour in range(0, 1):

            hour_array = array[array['hour'] == hour]

            predictions = []
            targets = []

            for count in range(0, len(hour_array) - model_range):

                model_data = hour_array[count: count + model_range]

                last_price = model_data[-2]
                prediction_objective = model_data[-1]

                differences = numpy.diff(model_data[0:-1]['congestion'])

                # remove top 10% and bottom 10% from the distribution
                differences = numpy.sort(differences)
                size = len(differences)
                percentile = round(size / 10, 0)
                differences = differences[percentile : size - percentile]

                # fit the distribution using kernel density estimate
                differences_pdf = stats.gaussian_kde(differences)

                generated_differences = differences_pdf.resample(iterations)

                target_distribution = generated_differences + last_price['congestion']
                target_pdf = stats.gaussian_kde(target_distribution)


                x = numpy.linspace(numpy.min(target_distribution),
                                   numpy.max(target_distribution),
                                   1000)
                y = target_pdf(x)

                predictions.append(x[numpy.argmax(y)])
                targets.append(prediction_objective['congestion'])

            targets = numpy.asarray(targets)
            predictions = numpy.asarray(predictions)

            error = numpy.sum((targets - predictions) ** 2) / len(predictions)

            plt.plot(targets - predictions)
            plt.show()
            plt.plot(predictions, 'g-', targets, 'r-')
            plt.show()