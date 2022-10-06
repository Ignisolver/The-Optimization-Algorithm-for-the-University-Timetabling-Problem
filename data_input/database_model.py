from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine, Column, Integer, String
engine = create_engine("sqlite:///:memory:", echo=True)
Base = declarative_base()