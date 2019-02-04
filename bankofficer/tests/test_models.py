import unittest
from datetime import datetime, timedelta

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from bankofficer.db2handler import DB2Hndler
from bankofficer.models import BaseModel, AccountOfficerRequest,\
    RequestService, Score


schema = 'ACC_OFF'
practice_table = 'account_officers'
engine = create_engine('sqlite:///practice_db')
BaseModel.metadata.drop_all(engine)
BaseModel.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
sqlite_connection = engine.connect()
base_time = datetime.today()-timedelta(2)
start_date = base_time.strftime('%Y-%m-%d') + ' 00:00:00'
end_date = base_time.strftime('%Y-%m-%d') + ' 23:59:00'


class TestModel(unittest.TestCase):

    def test_account_officers(self):
        handler = DB2Hndler(
            host='192.168.53.36',
            port=50000,
            database='bamlo140',
            username='devusr',
            password='usr140dv'
        )
        officer_request_statement =\
            "SELECT name, family, personnel_id, branch_code, branch_name,"\
            " requests.id as request_id, requests.req_count as request_count"\
            " FROM acc_off.account_officers as officers"\
            " JOIN acc_off.assigns as assigns"\
            " ON assigns.officer_id = officers.id"\
            " JOIN acc_off.requests as requests"\
            " ON requests.assign_id = assigns.id"\
            " AND requests.creation_date > '{}'"\
            " AND requests.creation_date < '{}'".format(start_date, end_date)

        officer_request = handler.fetch_statement_data(officer_request_statement)
        for officer in officer_request:
            new_officer = AccountOfficerRequest(**officer)
            session.add(new_officer)
        session.commit()


        request_service_statement = \
            "SELECT services.description as description,"\
            " cat.desctipion as category, requests.id"\
            " FROM ACC_OFF.requests as requests"\
            " join acc_off.services as services"\
            " on requests.service_id = services.id"\
            " AND requests.creation_date > '{}'"\
            " AND  requests.creation_date < '{}'"\
            " join acc_off.service_categories as cat"\
            " on services.categoty_id = cat.id".format(start_date, end_date)
        requests = handler.fetch_statement_data(request_service_statement)
        assert requests is not None
        for request in requests:
            new_request = RequestService(**request)
            session.add(new_request)
        session.commit()

        scores_statement = \
            "SELECT scores.value, scores.service_complexity_value as service_complexity,"\
            " requests.req_count as request_count, requests.id as request_id"\
            " FROM acc_off.scores as scores"\
            " join acc_off.requests as requests"\
            " on scores.request_id = requests.id"\
            " AND requests.creation_date > '{}'"\
            " AND  requests.creation_date < '{}'".format(start_date, end_date)

        scores = handler.fetch_statement_data(scores_statement)
        assert scores is not None
        for score in scores:
            new_score = Score(**score)
            session.add(new_score)
        session.commit()

        query_account_officers = session.query(AccountOfficerRequest).all()
        assert query_account_officers is not None

        query_request_services = session.query(RequestService).all()
        assert query_request_services is not None

        query_scores = session.query(Score).all()
        assert query_scores is not None

        # test relation ship
        officers = session.query(AccountOfficerRequest)
        assert officers[0].assigned_request is not None

        scores = session.query(Score).all()
        assert scores[0].assigned_request is not None
