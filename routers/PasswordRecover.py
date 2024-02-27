from fastapi import APIRouter, HTTPException
from database import Recover_Password, get_user_by_email
from models import PasswordRecover, Email

router = APIRouter()

@router.put("/RecoverPassword")
async def recoverPassword(passwordRecover: PasswordRecover):
    Updated = Recover_Password(passwordRecover.email, passwordRecover.password)
    if Updated:
        return {"message":"password updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="User_Not_Found")
    
@router.post("/EmailRecoverExist")
async def EmailRecoverExist(email: Email):
    user = get_user_by_email(email.email)
    if user:
        return {"message":"Email_Exist"}
    else:
        raise HTTPException(status_code=401, detail="Email_Not_Exist")
