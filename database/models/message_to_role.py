from sqlalchemy import Column, Integer
from database.orm import Base


class MessageToRole(Base):
    __tablename__ = 'messages_to_roles'

    message_id = Column('message_id', Integer, primary_key=True)
    role_id = Column('role_id', Integer, nullable=False)
