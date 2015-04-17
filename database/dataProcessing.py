__author__ = 'geoffrey'

from datetime import timedelta
import database.interface

def convert_outage_date_range_to_hour_ending():

    outage_key_list = get_all_outage_keys()

    for key in outage_key_list:
        sql_statement = 'SELECT * FROM cwpenergy.pjm_oper_outages ' \
                        'WHERE ticket_id = ' + str(key[0]) + ' AND b3_text=\'' + key[1] + '\''

        selection = database.interface.select_from_db(sql_statement)

        for element in selection:
            insert_list = convert_outage_range_to_hour_ending(element)

            insertion_statement = 'INSERT INTO cwpenergy.pjm_oper_line_outages_he VALUES '

            on_duplicate = 'ON DUPLICATE KEY UPDATE zone=VALUES(zone)'

            database.interface.insert_into_db(insertion_statement + ', '.join(insert_list) + on_duplicate)



def get_all_outage_keys():


    sql_statement = 'SELECT ticket_id, b3_text ' \
                   'FROM cwpenergy.pjm_oper_outages ' \
                   'WHERE type = \'LINE\' ' \
                   'GROUP BY CONCAT(ticket_id, b3_text)'

    return database.interface.select_from_db(sql_statement)


def convert_outage_range_to_hour_ending(date_range_selection):

    ticket_id = date_range_selection[0]
    b1_name = date_range_selection[1]
    b2_name = date_range_selection[2]
    b3_text = date_range_selection[3]
    status = date_range_selection[4]
    outage_type = date_range_selection[5]
    zone = date_range_selection[6]
    start = date_range_selection[7]
    end = date_range_selection[8]

    hour_ending_list = []

    while start <= end :

        start = start + timedelta(hours=1)

        element = '(\'' + start.strftime("%Y-%m-%d %H:%M:%S") + \
                  '\', ' + str(ticket_id) + ', \'' + b1_name + \
                  '\', \'' + b2_name + '\', \'' + b3_text + \
                  '\', \'' + status + '\', \'' + outage_type + \
                  '\', \'' + zone + '\')'

        hour_ending_list.append(element)

    return hour_ending_list


if __name__ == '__main__':

    convert_outage_date_range_to_hour_ending()