from fastapi import APIRouter, HTTPException
from database import delete_report

router = APIRouter()

@router.delete("/deleteOneReport/{report_id}")
async def deleteOneReport(report_id: int):
    deleted = delete_report(report_id)
    if deleted:
        return {"message": "Report deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Report not found")