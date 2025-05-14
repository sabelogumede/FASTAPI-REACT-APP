# Import SQLAlchemy core components for database connection and ORM support
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Define the database URL — using SQLite database named 'finance.db' in the current directory
URL_DATABASE = "sqlite:///./finance.db"

# Create a database engine
# The 'check_same_thread=False' is required for SQLite when using it with multiple threads (as FastAPI does)
engine = create_engine(URL_DATABASE, connect_args={"check_same_thread": False})

# Create a configured "Session" class bound to the engine
# autocommit=False means changes must be manually committed
# autoflush=False disables automatic flushing of changes to the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for declarative class definitions (models will inherit from this)
Base = declarative_base()
