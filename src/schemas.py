from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, date


class ContactModel(BaseModel): # for post (create)

    name: str = Field(min_length=2, max_length=20)
    surname: str = Field(min_length=2, max_length=20)
    email: str = EmailStr 
    phone: str = Field(min_length=2, max_length=20)
    birthday: date
    additional: str = Field()
    

class ResponseContact(BaseModel): # for get
    id: int = 1
    name: str
    surname: str
    email: str = EmailStr
    phone: str
    birthday: date
    additional: str 
    created_at: datetime
    updated_at: datetime

    class Config:
        #orm_mode = True
        from_attributes = True
