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

    return result


if __name__ == '__main__':
    connection = connect_to_db()
    statement = "SELECT o.name, o.family, o.personnel_id, o.branch_code, s.value as score" \
                " FROM ACC_OFF.ACCOUNT_OFFICERS as o " \
                "JOIN ACC_OFF.ASSIGNS as a on o.id = a.officer_id " \
                "JOIN ACC_OFF.REQUESTS as r on a.id =r.assign_id " \
                "join ACC_OFF.SCORES as s on r.id = s.request_id ORDER BY o.name"

    query_result = handel_statement(connection, statement)
    print(dump_query(query_result))
