from sqlalchemy import Column, String

from database.orm import Base


class Command(Base):
    __tablename__ = 'commands'

    command = Column('command', String, primary_key=True)
    response = Column('response', String, nullable=False)
