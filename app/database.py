from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

# Example MySQL connection URI
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:dewas%40123@127.0.0.1/fastapi_blog"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
