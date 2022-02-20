from database.orm import Base
from database.repositories.repository import Repository
from sqlalchemy.orm import session
from sqlalchemy import update, select


class HelperRepository(Repository):
    def __init__(self, sessionmaker: session, user_rank_model: Base, helper_range_model: Base):
        super(HelperRepository, self).__init__(sessionmaker=sessionmaker, model=user_rank_model)
        self.user_model = user_rank_model
        self.helper_model = helper_range_model

    def add_points_to_user(self, user_id, points):
        session = self.sessionmaker()
        user_points = session.execute(select(self.user_model.points).where(self.user_model.user_id == user_id)).scalars().first()
        if user_points is None:
            user = self.user_model()
            user.user_id = user_id
            user.points = points
            session.add(user)
        else:
            session.execute(update(self.user_model).where(self.user_model.user_id == user_id).values(points=user_points+points))
        session.commit()
        session.close()

    def role_id_user_should_have(self, user_id) -> int:
        session = self.sessionmaker()
        user_points = session.execute(select(self.user_model.points).where(self.user_model.user_id == user_id)).scalars().first()
        role_id = session.execute(select(self.helper_model.role_id).where(self.helper_model.bottom_limit <= user_points)).scalars().first()
        session.close()
        return role_id

    def get_whole_rank(self) -> list:
        session = self.sessionmaker()
        users = session.execute(select(self.user_model).order_by(self.user_model.points.desc())).scalars().all()
        session.close()
        return users
