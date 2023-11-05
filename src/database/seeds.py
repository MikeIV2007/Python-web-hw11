from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker
from datetime import date

from models import Base, Contact
from connect import URI


engine = create_engine(URI)
Session = sessionmaker(bind=engine)
session = Session()

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

fake = Faker()

# Create 30 fake contacts and insert them into the database
for _ in range(50):
    contact = Contact(
        name=fake.first_name(),
        surname=fake.last_name(),
        email=fake.email(),
        phone=fake.phone_number(),
        birthday=fake.date_of_birth(minimum_age=18, maximum_age=65),
        additional=fake.text(max_nb_chars=20),  # Limit text to 20 characters
    )

    session.add(contact)

session.commit()

# to run the script move to src/database derictory and run: py seeds.py
