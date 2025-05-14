# Import FastAPI framework and required components for API handling and database dependency injection
from fastapi import FastAPI, HTTPException, Depends
from typing import Annotated, List
from sqlalchemy.orm import Session
from pydantic import BaseModel

# Import the database session and engine setup
from database import SessionLocal, engine

# Import the ORM models
import models

# Import CORS middleware to allow frontend-backend communication
from fastapi.middleware.cors import CORSMiddleware

# Initialize the FastAPI application
app = FastAPI()

# Define allowed frontend origins (e.g., React app running on localhost:3000)
origins = [
    'http://localhost:3000'
]

# Enable CORS middleware to allow cross-origin requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow only specific origins
)

# Define a base Pydantic model for validating and parsing incoming transaction data
class TransactionBase(BaseModel):
    amount: float
    category: str
    description: str
    is_income: bool
    date: str

# Extend the base model for responses to include the transaction ID
class TransactionModel(TransactionBase):
    id: int

    # Enable ORM compatibility so Pydantic can work with SQLAlchemy models
    class Config:
        from_attributes = True

# Dependency to get a database session for each request
def get_db():
    db = SessionLocal()  # Create a new session
    try:
        yield db  # Provide the session to the request
    finally:
        db.close()  # Ensure the session is closed after the request is done

# Type alias for injecting the DB session into route handlers using Depends
db_dependency = Annotated[Session, Depends(get_db)]

# Automatically create all database tables based on the defined SQLAlchemy models
models.Base.metadata.create_all(bind=engine)


# Route for creating a new transaction
@app.get("/")
def read_root():
    return {"message": "FastAPI backend is running!"}



@app.post("/transactions/", response_model=TransactionModel)
async def create_tansaction(transaction: TransactionBase, db: db_dependency):
    # Create a new Transaction instance from the request data
    db_transaction = models.Transaction(**transaction.model_dump())
    
    # Add the new transaction to the database session
    db.add(db_transaction)
    db.commit()  # Commit the transaction (save to DB)
    db.refresh(db_transaction)  # Refresh to get the new ID and updated state from DB

    # Return the created transaction
    return db_transaction


@app.get("/transactions", response_model=List[TransactionModel])
async def read_transactions(db: db_dependency, skip: int = 0, limit: int = 100):
    transactions = db.query(models.Transaction).offset(skip).limit(limit).all()
    return transactions