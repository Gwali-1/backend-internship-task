from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

SQLITE_DATABASE_URL = "sqlite:///./records.db"
engine = create_engine(SQLITE_DATABASE_URL)
SESSION_FACTORY =   sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
