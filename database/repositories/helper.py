from sqlalchemy import update, select
from sqlalchemy.orm import session

from database.orm import Base
from database.repositories.repository import Repository


class HelperRepository(Repository):
    def __init__(self, sessionmaker: session, user_rank_model: Base, helper_range_model: Base, helper_reward_model: Base):
        super(HelperRepository, self).__init__(sessionmaker=sessionmaker, model=user_rank_model)
        self.user_rank_model = user_rank_model
        self.range_model = helper_range_model
        self.reward_model = helper_reward_model

    def add_points_to_user(self, user_id, points):
        session = self.sessionmaker()
        user_points = session.execute(
            select(self.user_rank_model.points).where(self.user_rank_model.user_id == user_id)).scalars().first()
        if user_points is None:
            user = self.user_rank_model()
            user.user_id = user_id
            user.points = points
            session.add(user)
        else:
            session.execute(
                update(self.user_rank_model).where(self.user_rank_model.user_id == user_id).values(points=user_points + points))
        session.commit()
        session.close()

    def role_id_user_should_have(self, user_id) -> int:
        session = self.sessionmaker()
        user_points = session.execute(select(self.user_rank_model.points).where(self.user_rank_model.user_id == user_id)).scalars().first()
        role_id = session.execute(select(self.range_model.role_id).order_by(self.range_model.bottom_threshold.desc()).where(self.range_model.bottom_threshold<= user_points)).scalars().first()
        session.close()
        return role_id

    def get_whole_rank(self) -> list:
        session = self.sessionmaker()
        users = session.execute(select(self.user_rank_model).order_by(self.user_rank_model.points.desc())).scalars().all()
        session.close()
        return users

    def get_reward(self, emoji_name) -> int:
        session = self.sessionmaker()
        reward = session.execute(select(self.reward_model.reward).where(self.reward_model.emoji_name == emoji_name)).scalars().first()
        session.close()
        return reward

    def get_emojis(self) -> list:
        session = self.sessionmaker()
        emojis = session.execute(select(self.reward_model.emoji_name)).scalars().all()
        session.close()
        return emojis
        
    def get_roles(self) -> list:
        session = self.sessionmaker()
        roles = session.execute(select(self.range_model.role_id)).scalars().all()
        session.close()
        return roles
    
    def remove_user(self, user_id):
        session = self.sessionmaker()
        session.query(self.model).filter_by(user_id=user_id).delete()
        session.commit()
        session.close()
