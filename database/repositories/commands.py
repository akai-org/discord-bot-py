from database.repositories.repository import Repository
from sqlalchemy import select


class CommandsRepository(Repository):

    def available_commands(self) -> list:
        session = self.sessionmaker()
        commands = session.execute(select(self.model.command)).scalars().all()
        session.close()
        return commands

    def response_for_command(self, command) -> str:
        session = self.sessionmaker()
        response = session.execute(select(self.model.response).where(self.model.command == command)).scalars().first()
        session.close()
        return response
