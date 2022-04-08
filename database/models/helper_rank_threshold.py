from sqlalchemy import Column, Integer
from database.orm import Base


class HelperRankThreshold(Base):
    __tablename__ = 'helper_ranges'

    bottom_threshold = Column('bottom_threshold', Integer, primary_key=True)
    role_id = Column('role_id', Integer, nullable=False)
