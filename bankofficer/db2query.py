
import os

import ibm_db

from bankofficer import MAIN_DIRECTORY
from bankofficer.exeptions import DB2Exception
from bankofficer.result_writer import ResultWriter
from bankofficer.constants import CSV_FIELDS


PORT = 50000
TIME_STAMP = '2018-07-01 00:00:00.000000'
HOST = 'localhost'


def connect_to_db(database='ACCOFFDB', host=HOST,port=PORT,
                  username='db2inst1', password='db2inst1-pwd'):

    connection = None
    try:
        connection = ibm_db.connect(
            "DATABASE={};HOSTNAME={};PORT={};PROTOCOL=TCPIP;"
            "UID={};PWD={};" \
            .format(database, host, port, username, password), "", ""
        )
    except Exception:
        raise DB2Exception(ibm_db.conn_errormsg())

    return connection


def handel_statement(connection, statement):
    query_result = None

    try:
        query_result = ibm_db.exec_immediate(connection, statement)
    except Exception:
        raise DB2Exception(ibm_db.stmt_errormsg())

    return query_result


def dump_query(query):
    result = []
    while ibm_db.fetch_row(query):
        result.append(ibm_db.fetch_assoc(query))

    # delete the last element which is None
    del result[-1]
    return result


def write_to_excel(filename, data):
    if os.path.exists(filename):
        os.remove(filename)


def translate_query_fields(dumped_query: list):
    result = []
    for element in dumped_query:
        result.append({CSV_FIELDS[key.lower()]: value
                       for key, value in element.items()})

    return result


def create_db2_report(database_string: list, start_date, end_date):
    connection = connect_to_db(*database_string)
    statement = "SELECT o.name, o.family, o.branch_code as shoab_code,"\
        "o.branch_name as shoab, SUM(value) as score,"\
        "COUNT(s.request_id) as request_count,"\
        "se.title FROM ( ( ( ACC_OFF.scores as s INNER JOIN "\
        "ACC_OFF.requests as r  ON s.request_id = r.id "\
        "AND s.ISSUE_DATE > TIMESTAMP('{}')"\
        "AND  s.ISSUE_DATE < TIMESTAMP('{}')"\
        "INNER JOIN ACC_OFF.services as se on r.service_id = se.id )"\
        "INNER JOIN ACC_OFF.assigns as a on r.assign_id = a.id)"\
        "INNER JOIN ACC_OFF.account_officers as o  ON a.officer_id = o.id)"\
        "group by o.name, o.family, o.branch_code, o.branch_name, se.title"\
        .format(start_date, end_date)

    query_result = handel_statement(connection, statement)
    dumped_query = dump_query(query_result)
    translated_query = translate_query_fields(dumped_query)
    query_fieldnames = [key for key, value in translated_query[0].items()]
    writer = ResultWriter(translated_query)
    writer.write_to_csv(
        os.path.join(MAIN_DIRECTORY, 'data/bank_officer.csv'),
        query_fieldnames
    )
    writer.write_to_excel(
        os.path.join(MAIN_DIRECTORY, 'data/bank_officer.xlsx')
    )
