import csv
import os

import ibm_db

from exeptions import DB2Exception

PORT = 50000
HOST = 'localhost'


def connect_to_db(database='ACCOFFDB', port=PORT, host=HOST,
                  username='db2inst1', password='db2inst1-pwd'):

    connection = None
    try:
        connection = ibm_db.connect(
            f"DATABASE={database};HOSTNAME={host};PORT={port}"
            f";PROTOCOL=TCPIP;UID={username};PWD={password};", "", ""
    )
    except Exception as e:
        raise DB2Exception(ibm_db.conn_errormsg())


    return connection


def handel_statement(connection, statement):
    query_result = None

    try:
        query_result = ibm_db.exec_immediate(connection, statement)
    except:
        raise DB2Exception(ibm_db.stmt_errormsg())

    return query_result


def dump_query(query):
    result = []
    while ibm_db.fetch_row(query):
        result.append(ibm_db.fetch_assoc(query))

    final_result = result
    return final_result


def write_to_csv(csvname, fieldnames, data:list):
    if os.path.exists(csvname):
        os.remove(csvname)
    with open(csvname, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for element in data:
            if isinstance(element, dict):
                writer.writerow(element)


if __name__ == '__main__':
    connection = connect_to_db()
    statement = "SELECT o.name, o.family, o.branch_code as shoab_code, SUM(value) as score,"\
                " COUNT(s.request_id) as request_count, se.title"\
                " FROM (((ACC_OFF.scores as s INNER JOIN ACC_OFF.requests as r ON s.request_id = r.id"\
                " INNER JOIN ACC_OFF.services as se on r.service_id = se.id)"\
                " INNER JOIN ACC_OFF.assigns as a on r.assign_id = a.id)"\
                " INNER JOIN ACC_OFF.account_officers as o ON a.officer_id = o.id)"\
                " group by o.name, o.family, o.branch_code, se.title"

    query_result = handel_statement(connection, statement)
    dumped_query = dump_query(query_result)
    query_fieldnames = [key for key, value in dumped_query[0].items()]
    write_to_csv('accountoffice.csv', query_fieldnames, dumped_query)

