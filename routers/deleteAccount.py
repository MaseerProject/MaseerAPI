from fastapi import APIRouter, HTTPException
from database import delete_user_account

router = APIRouter()

@router.delete("/deleteAccount/{user_id}")
async def deleteAccount(user_id: int):
    deleted = delete_user_account(user_id)
    if deleted:
        return {"message": "User account deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="User_Not_Found")