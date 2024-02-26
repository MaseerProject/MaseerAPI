from fastapi import APIRouter, HTTPException
from database import get_userData


router = APIRouter()

@router.get("/userData/{user_id}")
async def get_user_data(user_id: int):
    user_data = get_userData(user_id)
    if user_data:
        return user_data
    else:
        raise HTTPException(status_code=404, detail="User_Not_Found")
    


    
