from sqlalchemy.orm import session

from database.orm import Base


class Repository:
    def __init__(self, sessionmaker: session, model: Base):
        self.sessionmaker = sessionmaker
        self.model = model
