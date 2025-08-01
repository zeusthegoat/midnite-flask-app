# Idempotent seeding 

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Event

DATABASE_URL = "postgresql://midnite_user:midnite_pass@db:5432/midnite"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def seed_events():
    sample_data = [
        {
            "user_id": 1,
            "event_type": "deposit",
            "amount": 100.0,
            "timestamp": 1725100000,
        },
        {
            "user_id": 2,
            "event_type": "withdrawal",
            "amount": 45.5,
            "timestamp": 1725100600,
        },
        {
            "user_id": 1,
            "event_type": "deposit",
            "amount": 250.0,
            "timestamp": 1725101200,
        },
    ]

    with Session() as session:
        existing_count = session.query(Event).count()
        if existing_count > 0:
            print(f"Seed skipped: {existing_count} events already exist.")
            return

        for item in sample_data:
            event = Event(**item)
            session.add(event)
        session.commit()
        print(f"Seed data added: {len(sample_data)} events inserted.")

if __name__ == "__main__":
    seed_events()
