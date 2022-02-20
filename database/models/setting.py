from sqlalchemy import Column, String
from database.orm import Base


class Setting(Base):
    __tablename__ = 'settings'

    key = Column('key', String, primary_key=True)
    value = Column('value', String, nullable=False)
