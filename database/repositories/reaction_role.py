from database.repositories.repository import Repository
from sqlalchemy import select


class ReactionRoleRepository(Repository):
    def fetch_associated_role_id(self, emoji) -> int:
        session = self.sessionmaker()
        role_id = session.execute(select(self.model.role_id).where(self.model.emoji == emoji)).scalars().first()
        session.close()
        return role_id
