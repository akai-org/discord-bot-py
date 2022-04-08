from email.policy import default
from sqlalchemy import Column, Integer
from database.orm import Base


class HelperRank(Base):
    __tablename__ = 'helper_ranking'

    user_id = Column('user_id', Integer, primary_key=True)
    points = Column('points', Integer, default=0)
