from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLITE_FILE = 'db.sqlite3'

engine = create_engine(f'sqlite:///{SQLITE_FILE}')
Base = declarative_base()
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
