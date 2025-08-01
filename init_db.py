# one time connection and table creation script. !!! DO NOT USE UNLESS DATABASE HAS BEEN RESET !!!!

from sqlalchemy import create_engine
from models import Base

DATABASE_URL = "postgresql://midnite_user:midnite_pass@db:5432/midnite"
engine = create_engine(DATABASE_URL)

print("Creating all tables...")
Base.metadata.create_all(engine)
print("Tables created successfully.")
