from sqlalchemy import Column, String, Integer
from database.orm import Base


class HelperReward(Base):
    __tablename__ = 'helper_rewards'

    reward = Column('reward', Integer, primary_key=True)
    emoji_name = Column('emoji_name', String, nullable=False)
