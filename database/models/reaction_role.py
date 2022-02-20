from sqlalchemy import Column, String
from database.orm import Base


class ReactionRole(Base):
    __tablename__ = 'reaction_roles'

    emoji = Column('emoji', String, primary_key=True)
    role_id = Column('role_id', String, nullable=False)
