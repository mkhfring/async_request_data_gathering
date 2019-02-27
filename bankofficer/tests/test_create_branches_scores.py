import unittest
from datetime import datetime, timedelta

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func


from bankofficer.db2handler import DB2Hndler
from bankofficer.models import BaseModel


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


class TestCreateBranchesReport(unittest.TestCase):

    def test_create_report_without_branch(self):
        handler = DB2Hndler(
            host='192.168.53.36',
            port=50000,
            database='bamlo140',
            username='devusr',
            password='usr140dv'
        )
        statement = "SELECT request_score.request_count, request_score.score"\
                    ", service_category.description, service_category.category"\
                    " FROM"\
                    " (SELECT s.id as service_id, s.description, sc.desctipion"\
                    " as category FROM ACC_OFF.SERVICES as s"\
                    " JOIN ACC_OFF.SERVICE_CATEGORIES as sc"\
                    " ON s.CATEGOTY_ID = sc.ID) service_category JOIN"\
                    "(SELECT SUM(score.value * score.service_complexity_value)"\
                    " as score, r.service_id, SUM(r.req_count) as request_count"\
                    " FROM ACC_OFF.scores as score JOIN ACC_OFF.requests as r"\
                    "  ON score.request_id = r.id"\
                    "  AND r.creation_date > '{}'"\
                    "  AND r.creation_date <'{}'"\
                    " GROUP BY r.service_id) request_score"\
                    " ON service_category.service_id = request_score.service_id"\
            .format(start_date, end_date)

        total_services_score = handler.fetch_statement_data(statement)
        assert isinstance(total_services_score, list)
        assert len(total_services_score) > 0

        statement2 = "SELECT SUM(s.value * s.service_complexity_value)"\
                     " as score, r.service_id, r.assign_id"\
                     " FROM ACC_OFF.scores as s JOIN ACC_OFF.requests as r"\
                     " ON s.request_id = r.id"\
                     " AND r.creation_date > '2019-01-21 00:00:00'"\
                     " AND r.creation_date <'{}'"\
                     " GROUP BY r.service_id, r.assign_id".format(end_date)
        request_scores = handler.fetch_statement_data(statement2)
        assert isinstance(request_scores, list)
        assert len(request_scores) > 0
