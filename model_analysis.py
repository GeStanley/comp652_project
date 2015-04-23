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


def generate_forecast_targets(number_of_targets, data, window_size, outlier_percentage):

    predictions = []
    targets = []

    for count in range(0, number_of_targets):

        model_data = data[count: count + window_size]

        last_price = model_data[-2]
        prediction_objective = model_data[-1]

        differences = numpy.diff(model_data[0:-1]['congestion'])

        # remove top 10% and bottom 10% from the distribution
        differences = numpy.sort(differences)
        size = len(differences)
        percentile = round(size * outlier_percentage, 0)
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

    return targets, predictions


def calculate_forecast_error(price_history, hour, model_range, percentage):

    hour_array = price_history[price_history['hour'] == hour]

    predictions, targets = generate_forecast_targets(len(hour_array) - model_range,
                                                 hour_array,
                                                 model_range,
                                                 percentage)

    targets = numpy.asarray(targets)
    predictions = numpy.asarray(predictions)

    return numpy.sum((targets - predictions) ** 2) / len(predictions)


if __name__ == '__main__':


    iterations = 10

    dt = numpy.dtype([('time_id', 'S32'), ('congestion', 'f8'), ('hour', 'i8')])

    all_data_array = numpy.loadtxt('hour.txt', dtype=dt, delimiter=',')

    # the most efficient history size was 30 days
    for model_range in range(30, 31):

        validation_errors = numpy.zeros(50)

        for percentage in range(0, 25, 1):
            print percentage
            range_error = numpy.zeros(24)

            for hour in range(0, 24):

                error = calculate_forecast_error(all_data_array, hour, model_range, percentage/100.0)

                range_error[hour] = error

            average_error = numpy.average(range_error)
            print average_error
            validation_errors[percentage] = average_error

        numpy.savetxt('outlier_error.txt', validation_errors, fmt=['%5.3f'], delimiter=',')