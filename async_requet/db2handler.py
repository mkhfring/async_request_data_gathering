import ibm_db
import ibm_db_sa

from async_requet.exeptions import DB2Exception


class AbtractDatabaseHandler:

    def __init__(self, host, port, database, username, password):
        self.host = host
        self.port = port
        self.database = database
        self.username = username
        self.password = password
        self.connection = None
        self.query_result = None


class DB2Hndler(AbtractDatabaseHandler):

    def __init__(self, host, port, database, username, password):
        super().__init__(host, port, database, username, password)

    def connect(self):

        try:
            connection = ibm_db.connect(
                "DATABASE={};HOSTNAME={};PORT={};PROTOCOL=TCPIP;"
                "UID={};PWD={};" \
                    .format(
                    self.database,
                    self.host,
                    self.port,
                    self.username,
                    self.password
                ), "", ""
            )
        except Exception:
            raise DB2Exception(ibm_db.conn_errormsg())

        self.connection = connection

    def fetch_statement_data(self, statement):
        self.connect()

        try:
            self.query_result = ibm_db.exec_immediate(self.connection, statement)
        except Exception:
            raise DB2Exception(ibm_db.stmt_errormsg())

        return self._dump_query(self.query_result)

    def _dump_query(self, query):
        result = []
        ibm_fetched_query = ibm_db.fetch_assoc(query)

        while ibm_fetched_query:
            result.append(ibm_fetched_query)
            ibm_fetched_query = ibm_db.fetch_assoc(query)

        return result
