from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

from app.database.models import Base
from dotenv import load_dotenv

load_dotenv()

# define fallback url if .env is not loaded, change to yours
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:password@localhost/test_db")

# sql alchemy engine
# set echo to True to see SQL queries in logs
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    echo=False
)

# each instance of SessionLocal will be a database session
# autoflush=False: prevents flushing objects to the database automatically after every change
# autocommit=False: ensures changes are not committed automatically
# bind=engine: binds this session to our created engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    print("Attempting to create database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully or already exist.")
    except Exception as e:
        print(f"Error creating database tables: {e}")
        # or raise the exception, or graceful shutdown for real prod purposes