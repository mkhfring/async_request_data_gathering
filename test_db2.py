import unittest

import ibm_db

from db2query import connect_to_db
from exeptions import DB2Exception


class TestDB2Connection(unittest.TestCase):

    def test_connection(self):
        connection = connect_to_db()
        assert ibm_db.active(connection) is True
