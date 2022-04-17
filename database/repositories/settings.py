from database.repositories.repository import Repository


class SettingsRepository(Repository):
    def at_key(self, key: str) -> str:
        session = self.sessionmaker()
        value = session.query(self.model).filter_by(key=key).first().value
        session.close()
        return value
