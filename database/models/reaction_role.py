from sqlalchemy import Column, String, Integer
from database.orm import Base


class ReactionRole(Base):
    __tablename__ = 'reaction_roles'

    emoji = Column('emoji', String, primary_key=True)
    role_id = Column('role_id', Integer, nullable=False)
