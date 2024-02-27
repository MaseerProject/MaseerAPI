from fastapi import APIRouter, HTTPException
from database import delete_user_reports

router = APIRouter()

@router.delete("/deleteUserReports/{user_id}")
async def deleteUserReports(user_id: int):
    deleted = delete_user_reports(user_id)
    if deleted:
        return {"message": "All reports have been deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Report not found")