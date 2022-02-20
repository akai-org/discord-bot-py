from sqlalchemy import Column, String, Integer
from database.orm import Base


class HelperRange(Base):
    __tablename__ = 'helper_ranges'

    bottom_limit = Column('bottom_limit', Integer, primary_key=True)
    response = Column('role_id', String, nullable=False)
