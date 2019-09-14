from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship


BaseModel = declarative_base()


class BotUser(BaseModel):
    __tablename__ = 'bot_user'

    id = Column(Integer, primary_key=True)
    access_hash = Column(String)
    peer_id = Column(String)

    @classmethod
    def is_exist(cls, session, id):
        user = session.query(cls).filter(cls.peer_id == id).one_or_none()
        return user

    @classmethod
    def delete_user(cls, user_id, session):
        current_user = session.query(cls) \
            .filter(cls.peer_id == user_id) \
            .one_or_none()

        session.delete(current_user)
        session.commit()


class AccountOfficerRequest(BaseModel):
    __tablename__ = 'officer_request'
    ID = Column(Integer, primary_key=True)
    NAME = Column(String)
    FAMILY = Column(String)
    BRANCH_CODE = Column(Integer)
    BRANCH_NAME = Column(String)
    PERSONNEL_ID = Column(Integer)
    TYPE = Column(String)
    SUPERVISOR_ID = Column(Integer, ForeignKey('officer_request.ID'))
    REQUEST_ID = Column(Integer, ForeignKey('service_request.ID'))
    REQUEST_COUNT = Column(Integer)
    REQUEST_STATUS = Column(String)
    assigned_request = relationship("RequestService")


class RequestService(BaseModel):
    __tablename__ = 'service_request'

    ID = Column(Integer, primary_key=True)
    DESCRIPTION = Column(String)
    CATEGORY = Column(String)


class Score(BaseModel):
    __tablename__ = 'score'

    ID = Column(Integer, primary_key=True)
    VALUE = Column(Integer)
    SERVICE_COMPLEXITY = Column(Integer)
    REQUEST_ID = Column(Integer, ForeignKey('service_request.ID'))
    REQUEST_COUNT = Column(Integer)
    assigned_request = relationship("RequestService")

