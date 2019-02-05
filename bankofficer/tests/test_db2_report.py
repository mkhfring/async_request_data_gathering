
import os
import unittest

import ibm_db

from bankofficer.db2query import connect_to_db, create_db2_report


HERE = os.path.dirname(os.path.realpath(__file__))
CSV_PATH = os.path.join(HERE, '../data/bank_officer.csv')
EXCEL_PATH = os.path.join(HERE, '../data/bank_officer.xlsx')


class TestDB2Connection(unittest.TestCase):

    def test_connection(self):
        connection = connect_to_db()
        create_db2_report(
            ['ACCOFFDB', 'localhost', 50000, 'db2inst1', 'db2inst1-pwd'],
            '2018-05-01 00:00:00.000000',
            '2018-07-01 00:00:00.000000'
        )
        assert os.path.exists(CSV_PATH)
        assert os.path.exists(EXCEL_PATH)
