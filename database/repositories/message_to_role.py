from sqlalchemy.sql import select

from database.orm import Session
from database.repositories.repository import Repository


class MessageToRoleRepository(Repository):
    def get_role_id(self, message_id) -> int:
        session = self.sessionmaker()
        query = select(self.model.role_id).where(self.model.message_id == message_id)
        role_id = session.execute(query).scalars().first()
        session.close()
        return role_id

    def create_message_role_association(self, message_id, role_id):
        session: Session = self.sessionmaker()
        session.add(self.model(message_id=message_id, role_id=role_id))
        session.commit()
        session.close()
