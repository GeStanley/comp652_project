__author__ = 'geoffrey'


from database import interface
from numpy.lib import recfunctions as rfn

import numpy

if __name__ == '__main__':

    east_to_west = interface.build_utc_array(51288, 51217, '2013-01-01 00:00:00', '2015-01-01 00:00:00')


    numpy.savetxt('east_to_west.txt', east_to_west, fmt=['%s', '%4.2f'], delimiter=',')

    dt = numpy.dtype([('time_id', 'S32'), ('congestion', 'f8')])

    array = numpy.loadtxt('east_to_west.txt', dtype=dt, delimiter=',')

    hours = map(lambda x: x[11:13], array['time_id'])

    b = rfn.append_fields(array, names='hour', data=hours, usemask=False)

    numpy.savetxt('hour.txt',b, fmt=['%s', '%4.2f', '%s'], delimiter=',')