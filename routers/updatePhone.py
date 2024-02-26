from fastapi import APIRouter, HTTPException
from database import update_phone_number
from models import PhoneUpdate

router = APIRouter()

@router.put("/updatePhone/{user_id}")
async def updatePhone(user_id: int, phone_update: PhoneUpdate):
    Updated = update_phone_number(user_id, phone_update.new_phone_number)
    if Updated:
        return {"message":"Phone number updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="User_Not_Found")