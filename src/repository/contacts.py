from datetime import date, timedelta
from sqlalchemy import and_, extract, or_
from sqlalchemy.orm import Session

from src.database.models import Contact
from src.schemas import ContactModel


async def get_all_contacts(limit: int, offset: int, db: Session):
    contacts = db.query(Contact)
    contacts = contacts.limit(limit).offset(offset).all()
    return contacts


async def get_contact_by_id(contact_id: int, db: Session):
    contact = db.query(Contact).filter_by(id=contact_id).first()
    return contact


async def get_contact_by_name(contact_name: str, limit: int, offset: int, db: Session):
    contacts = db.query(Contact).filter_by(name=contact_name)
    contacts = contacts.limit(limit).offset(offset)
    return contacts


async def get_contact_by_surname(contact_surname: str, limit: int, offset: int,db: Session):
    contacts = db.query(Contact).filter_by(surname=contact_surname)
    contacts = contacts.limit(limit).offset(offset)
    return contacts


async def get_contact_by_email(contact_email: str, db: Session):
    contact = db.query(Contact).filter_by(email=contact_email).first()
    return contact


async def get_contacts_with_birthdays_in_next_7_days(limit: int, offset: int, db: Session):
    # Calculate the current date and the date one week from now
    today = date.today()
    #today = datetime(2001, 12, 26).date() # for testing
    next_week = today + timedelta(days=7)

    # Extract the month and day from the Contact.birthday using SQLAlchemy's extract function
    birthday_month = extract('month', Contact.birthday)
    birthday_day = extract('day', Contact.birthday)

    if today.month == next_week.month:
        print (64, today.month == next_week.month)
        # Filter the contacts based on the month and day
        contacts = db.query(Contact).filter(
            birthday_month == today.month,
            birthday_day >= today.day,
            birthday_day <= next_week.day
        ).limit(limit).offset(offset)
        return contacts
    
    else:
        contacts = db.query(Contact).filter(
            or_(
                and_(
                    birthday_month == today.month,
                    today.day <= birthday_day,
                    birthday_day <= 31
                ),
                and_(
                    birthday_month == next_week.month,
                    1 <= birthday_day,
                    birthday_day <= next_week.day
                )
            )
        ).limit(limit).offset(offset)
        return contacts


async def create_contact(body: ContactModel, db: Session):
    contact = Contact(**body.model_dump())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(body: ContactModel, contact_id: int, db: Session):
    contact = db.query(Contact).filter_by(id=contact_id).first()
    if contact:
        contact.name = body.name
        contact.surname = body.surname
        contact.email = body.email
        contact.phone = body.phone
        contact.birthday = body.birthday
        contact.additional = body.additional
        db.commit()
    return contact

async def remove_contact(contact_id: int, db: Session):
    contact = db.query(Contact).filter_by(id=contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact

