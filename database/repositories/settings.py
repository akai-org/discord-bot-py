from database.repositories.repository import Repository


class SettingsRepository(Repository):
    def at_key(self, key: str) -> str:
        session = self.sessionmaker()
        value = session.query(self.model).filter_by(key=key).first().value
        session.close()
        return value

    def load_from_yaml(self, data):
        session = self.sessionmaker()
        for key, value in data.items():
            session.add(self.model(key=key, value=value))
        session.commit()
        session.close()
