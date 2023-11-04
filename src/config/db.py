from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from config.environment import env_data

SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{env_data.db_user}:{env_data.db_pass}@{env_data.db_host}:{env_data.db_port}/{env_data.db_name}"
Engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=env_data.debug, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=Engine)


def get_db_connection():
    db = scoped_session(SessionLocal)
    try:
        yield db
    finally:
        db.close()
