from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import get_settings

settings = get_settings()

SQLALCHEMY_DATEBASE_URL = (
    "mysql+mysqldb://"
    f"{settings.database_username}:{settings.database_password}"
    "@127.0.0.1/fastapi-ca"
)

engine = create_engine(SQLALCHEMY_DATEBASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()