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
                differences_pdf = stats.gaussian_kde(differences)

                generated_differences = differences_pdf.resample(iterations)

                target_distribution = generated_differences + last_price['congestion']
                target_pdf = stats.gaussian_kde(target_distribution)


                x = numpy.linspace(-100, 100, 1000)
                y = target_pdf(x)

                predictions.append(x[numpy.argmax(y)])
                targets.append(prediction_objective['congestion'])

            targets = numpy.asarray(targets)
            predictions = numpy.asarray(predictions)

            error = numpy.sum((targets - predictions) ** 2) / len(predictions)
            print error

            plt.plot(predictions, 'g-', targets, 'r-')
            plt.show()