# app/__init__.py
from .models import Base
from .database import engine

# Create all tables in the database
Base.metadata.create_all(bind=engine)
