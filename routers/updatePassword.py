from fastapi import APIRouter, HTTPException
from database import get_user_by_id, Update_Password
from models import PasswordUpdate

router = APIRouter()

@router.put("/updatePassword")
async def updatePassword(passwordUpdate: PasswordUpdate):
    user = get_user_by_id(passwordUpdate.user_id)
    if user:
        if user[1] == PasswordUpdate.old_password:
            Updated = Update_Password(PasswordUpdate.user_id, PasswordUpdate.new_pssword)
            if Updated:
                return {"message":"password updated successfully"}
            else:
                raise HTTPException(status_code=404, detail="User_Not_Found")
    else:
        raise HTTPException(status_code=401, detail="Email_Not_Exist")



