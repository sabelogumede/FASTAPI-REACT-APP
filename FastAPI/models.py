# Import the Base class from the database module for model inheritance
from database import Base

# Import SQLAlchemy column types
from sqlalchemy import Column, Integer, String, Boolean, Float

# Define the Transaction model which maps to the 'transactions' table in the database
class Transaction(Base):
    # Specify the table name in the database
    __tablename__ = 'transactions'

    # Primary key column with auto-incremented integer ID and index for faster lookup
    id = Column(Integer, primary_key=True, index=True)

    # Amount of the transaction (positive or negative), stored as a float
    amount = Column(Float)

    # Category of the transaction (e.g., 'Food', 'Salary', etc.)
    category = Column(String)

    # Optional description or note about the transaction
    description = Column(String)

    # Boolean flag indicating whether the transaction is income (True) or expense (False)
    is_income = Column(Boolean)

    # Date of the transaction, stored as a string (e.g., "2024-05-14")
    date = Column(String)
