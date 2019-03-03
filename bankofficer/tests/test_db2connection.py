import ibm_db
import pytest
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from bankofficer.accountofficer_migrate import db_connection, add_officer,\
    delete_officer, change_supervisors


TABLE_NAME = 'ACC_OFF.ACCOUNT_OFFICERS'
FIRSTNAME_INDEX = 5


class TestBankofficerRequest:

    def test_request_to_bankofficer(self):
        connection = db_connection(
            'db2inst1',
            'db2inst1-pwd',
            'localhost',
            50000,
            'ACCOFFDB'
        )
        with pytest.raises(OperationalError):
            bad_connection = db_connection(
                'db2inst1',
                'db2inst1-pwd',
                'localhost',
                50,
                'ACCOFFDB'
            )

        delete_officer(1111, connection)

        empty_result = connection.execute(
            "SELECT * FROM {} WHERE NAME = 'example'".format(TABLE_NAME)
        )

        # Check if the result is empty
        with pytest.raises(StopIteration):
            next(empty_result)

        add_officer(
            "'example'",
            "'example'",
            98911239,
            1111,
            "'example'",
            3333,
            2222222,
            connection
        )

        result = connection.execute(
            "SELECT * FROM {} WHERE NAME = 'naser'".format(TABLE_NAME)
        )

        record = next(result)
        assert record is not None
        assert record[FIRSTNAME_INDEX] == 'naser'

        change_supervisors(79575, 13565, connection)
        change_supervisors(13565, 79575, connection)
        connection.close()
