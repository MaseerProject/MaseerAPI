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