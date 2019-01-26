from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, Column, String


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
