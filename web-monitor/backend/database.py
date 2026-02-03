from sqlmodel import SQLModel, create_engine, Session
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="../.env")

from sqlalchemy import event

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./compost.db")

engine = create_engine(DATABASE_URL, echo=False)

# Enable Write-Ahead Logging (WAL) for concurrency
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.close()

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
