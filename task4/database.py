import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()

DB_NAME = os.getenv("DB_NAME", "customer_api_db")
DATABASE_URL = (
    f"postgresql+psycopg2://postgres:{os.getenv('DB_PASSWORD')}"
    f"@localhost:5432/{DB_NAME}"
)

engine = create_engine(DATABASE_URL, pool_size=5, max_overflow=10, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()