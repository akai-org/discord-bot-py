from sqlalchemy import Column, String, Integer

from database.orm import Base


class HelperReward(Base):
    __tablename__ = "helper_rewards"

    emoji_name = Column("emoji_name", String, primary_key=True)
    reward = Column("reward", Integer, nullable=False)
