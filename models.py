from fastapi import FastAPI
from pydantic import BaseModel

class UserCredentials(BaseModel):
    email: str
    password: str



class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    password: str

class PhoneUpdate(BaseModel):
    new_phone_number: str

class MailInfo(BaseModel):
    email: str
    otp_code: str


class PasswordRecover(BaseModel):
    email: str
    password: str

class PasswordUpdate(BaseModel):
    user_id: int
    old_password: str
    new_password: str

class Email (BaseModel):
    email: str