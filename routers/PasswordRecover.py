from fastapi import APIRouter, HTTPException
from database import Recover_Password
from models import PasswordRecover

router = APIRouter()

@router.put("/RecoverPassword")
async def recoverPassword(passwordRecover: PasswordRecover):
    Updated = Recover_Password(passwordRecover.email, passwordRecover.password)
    if Updated:
        return {"message":"password updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="User_Not_Found")