import unittest
from bankofficer.db2handler import DB2Hndler


schema = 'ACC_OFF'
practice_table = 'account_officers'


class DB2Connection(unittest.TestCase):

    def test_connection(self):
        handler = DB2Hndler(
            host='192.168.53.36',
            port=50000,
            database='bamlo140',
            username='devusr',
            password='usr140dv'
        )
        assert isinstance(handler, DB2Hndler)
        handler.connect()
        assert handler.connection is not None

        query_reult = handler.fetch_statement_data(
            'SELECT * from {}.{}'.format(schema, practice_table)
        )
        assert query_reult is not None
        assert isinstance(query_reult, list)
        assert isinstance(query_reult[0], dict)
