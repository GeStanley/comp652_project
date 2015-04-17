__author__ = 'geoffrey'


import MySQLdb as sql
import numpy
import numpy.lib.recfunctions as rfn
import pytz

ipAddress = '192.168.75.11'
userName = 'geoffrey'
passWord = 'frisKy03'
database = 'cwpenergy'

def build_utc_array(source, sink, start, end):

    source_prices = retrieve_node_data(source, start, end)
    sink_prices = retrieve_node_data(sink, start, end)

    source_data = []

    for element in source_prices:
        source_data.append((element[0].replace(tzinfo=pytz.timezone('EST')),
                            element[1],
                            element[2],
                            element[5]))

    sink_data = []

    for element in sink_prices:
        sink_data.append((element[0].replace(tzinfo=pytz.timezone('EST')),
                          element[1],
                          element[2],
                          element[5]))

    sink_dt = numpy.dtype([('time_id', 'S32'),
                      ('sink_node_id', 'i8'),
                      ('sink_rt_lmp', 'f8'),
                      ('sink_da_lmp', 'f8')])

    source_dt = numpy.dtype([('time_id', 'S32'),
                      ('source_node_id', 'i8'),
                      ('source_rt_lmp', 'f8'),
                      ('source_da_lmp', 'f8')])


    sink_array = numpy.array(sink_data, dtype=sink_dt)
    source_array = numpy.array(source_data, dtype=source_dt)

    joined = rfn.join_by('time_id', sink_array,
                                    source_array,
                                    jointype='inner', usemask=False)

    rt_congestion_rounded = numpy.round(joined['sink_rt_lmp'] - joined['source_rt_lmp'], 2)
    da_congestion_rounded = numpy.round(joined['sink_da_lmp'] - joined['source_da_lmp'], 2)
    profit_rounded = numpy.round(rt_congestion_rounded - da_congestion_rounded, 2)

    joined = rfn.append_fields(joined, 'rt_congestion', data=rt_congestion_rounded)
    joined = rfn.append_fields(joined, 'da_congestion', data=da_congestion_rounded)
    joined = rfn.append_fields(joined, 'profit', data=profit_rounded)

    return joined[['time_id', 'rt_congestion']]

def get_average_rt_lmp(start, end):

    db = sql.connect(host=ipAddress, user=userName, passwd=passWord, db=database)

    cursor = db.cursor()

    sql_retrieval = 'SELECT time_id, avg(rt_lmp) as avg_lmp ' \
                    'FROM cwpenergy.pjm_prices_current ' \
                    'WHERE time_id BETWEEN \'%s\' AND \'%s\' ' \
                    'GROUP BY time_id' % (start, end)

    try:

        cursor.execute(sql_retrieval)

        database_list = cursor.fetchall()

        average_lmp_data = []

        for element in database_list:
            average_lmp_data.append((element[0].replace(tzinfo=pytz.timezone('EST')),
                                     element[1]))

        data_types = numpy.dtype([('time_id', 'S32'),
                                  ('avg_lmp', 'f8')])

        return numpy.array(average_lmp_data, dtype=data_types)

    except sql.Error as e:
        try:
            print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
        except IndexError:
            print "MySQL Error: %s" % str(e)
            db.rollback()


def get_node_id_list(zone):

    db = sql.connect(host=ipAddress, user=userName, passwd=passWord, db=database)

    cursor = db.cursor()

    sql_retrieval = 'SELECT node_id ' \
                    'FROM cwpenergy.pjm_oper_nodes ' \
                    'WHERE area_name=\'' + zone + '\''

    try:

        cursor.execute(sql_retrieval)

        return cursor.fetchall()

    except sql.Error as e:
        try:
            print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
        except IndexError:
            print "MySQL Error: %s" % str(e)
            db.rollback()


def retrieve_node_data(node_id, start, end):


    db = sql.connect(host=ipAddress, user=userName, passwd=passWord, db=database)


    cursor = db.cursor()

    sql_retrieval = 'SELECT * FROM cwpenergy.pjm_prices_current ' \
                    'WHERE node_id=%s AND time_id ' \
                    'BETWEEN \'%s\' AND \'%s\'' % (node_id, start, end)

    try:


        cursor.execute(sql_retrieval)


        return cursor.fetchall()

    except sql.Error as e:
        try:
            print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
        except IndexError:
            print "MySQL Error: %s" % str(e)
            db.rollback()

def retrieve_load_forecast_data(start, end):

    db = sql.connect(host=ipAddress, user=userName, passwd=passWord, db=database)

    cursor = db.cursor()

    sql_retrieval = 'select time_id, load_forecast from (' \
                        'select distinct (concat(forecast_time_id, time_id)), ' \
                        'forecast_time_id, ' \
                        'time_id, ' \
                        'timediff(forecast_time_id, time_id) as time_dif, ' \
                        'region, ' \
                        'load_forecast ' \
                        'from cwpenergy.pjm_oper_current_load_forecast) as t ' \
                    'WHERE t.time_dif between \'-36:00:00\' AND \'-12:00:00\' ' \
                    'AND region=\'RTO COMBINED\' ' \
                    'AND time_id BETWEEN \'%s\' AND \'%s\';' % (start, end)


    try:

        cursor.execute(sql_retrieval)

        return cursor.fetchall()

    except sql.Error as e:
        try:
            print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
        except IndexError:
            print "MySQL Error: %s" % str(e)
            db.rollback()


def retrieve_wsi_weather_data(city, start, end):

    db = sql.connect(host=ipAddress, user=userName, passwd=passWord, db=database)

    cursor = db.cursor()

    sql_retrieval = 'SELECT h.time_id, h.temperature ' \
                    'FROM cwpenergy.wsi_cities_index as i, cwpenergy.wsi_hist_weather as h ' \
                    'WHERE h.airport_code=i.airport_code AND i.city=\'%s\''' ' \
                    'AND time_id BETWEEN \'%s\' AND \'%s\' ' \
                    'ORDER BY h.time_id asc' % (city, start, end)


    try:

        cursor.execute(sql_retrieval)

        return cursor.fetchall()

    except sql.Error as e:
        try:
            print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
        except IndexError:
            print "MySQL Error: %s" % str(e)
            db.rollback()


def select_from_db(sql_statement):

    db = sql.connect(host=ipAddress, user=userName, passwd=passWord, db=database)

    cursor = db.cursor()

    try:

        cursor.execute(sql_statement)

        return cursor.fetchall()

    except sql.Error as e:
        try:
            print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
        except IndexError:
            print "MySQL Error: %s" % str(e)
            db.rollback()



def insert_into_db(sql_insertion):

    db = sql.connect(host=ipAddress, user=userName, passwd=passWord, db=database)

    cursor = db.cursor()

    try:

        cursor.execute(sql_insertion)

        db.commit()

    except sql.Error as e:
        try:
            print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
        except IndexError:
            print "MySQL Error: %s" % str(e)
            db.rollback()

    db.close()