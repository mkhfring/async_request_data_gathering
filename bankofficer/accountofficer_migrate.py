from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError


def db_connection(username, password, host, port, db):
    connection = None
    engine = create_engine(
        "db2+ibm_db://{}:{}@{}:{}/{}" \
        .format(username, password, host, port, db)
    )
    try:
        connection = engine.connect()
    except OperationalError as e:
        raise e

    return connection


def add_officer(first_name, last_name, cell_phone, personel_id, branch_name,
                branch_code, ssn, connection):

    connection.execute(
        "INSERT INTO ACC_OFF.ACCOUNT_OFFICERS"
        "(NAME, FAMILy, CELL_PHONE_NO, PERSONNEL_ID,"
        "BRANCH_NAME, BRANCH_CODE, SSN) VALUES "
        "({}, {}, {}, {}, {}, {}, {})" \
        .format(
            first_name,
            last_name,
            cell_phone,
            personel_id,
            branch_name,
            branch_code,
            ssn
        )
    )


def delete_officer(personel_id, connection):
    connection.execute(
        "DELETE FROM ACC_OFF.ACCOUNT_OFFICERS where PERSONNEL_ID = {};" \
        .format(personel_id)
    )


def change_supervisors(previous_suppervisor, current_supervisor, connection):
    connection.execute(
       "UPDATE ACC_OFF.ACCOUNT_OFFICERS SET SUPERVISOR_ID = (SELECT ID FROM ACC_OFF.ACCOUNT_OFFICERS WHERE PERSONNEL_ID ={}) WHERE SUPERVISOR_ID = (SELECT ID FROM ACC_OFF.ACCOUNT_OFFICERS WHERE PERSONNEL_ID = {});".format(current_supervisor, previous_suppervisor)
    )

class BankOfficerDB:

    def __init__(username, password, host, port, db):
        self.connection = None
