from fastapi import APIRouter, HTTPException
from database import get_user_by_email
from models import UserCredentials


router = APIRouter()

@router.post("/login")
async def login(credentials: UserCredentials):
    email = credentials.email
    password = credentials.password
    user = get_user_by_email(email)
    if user:
        if user[1] == password:
            return {"message": "Login_Successful", "token": user[2]}
        else:
            raise HTTPException(status_code=402, detail="Invalid_Password")
    else:
        raise HTTPException(status_code=401, detail="Email_Not_Exist")