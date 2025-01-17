from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATEBASE_URL = "mysql+mysqldb://root:test@127.0.0.1/fastapi-ca"
engine = create_engine(SQLALCHEMY_DATEBASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine);

Base = declarative_base()