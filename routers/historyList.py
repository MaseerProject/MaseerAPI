from fastapi import APIRouter, HTTPException
from database import get_user_history

router = APIRouter()

@router.get("/historyList/{user_id}")
async def historyList(user_id: int):
    history = get_user_history(user_id)
    if history:

        history_list = [{"report_id": row[0],
                         "generation_date":  row[1].strftime("%Y-%m-%d"),
                         "generation_day": row[1].strftime("%A"),
                         "generation_time": row[1].strftime("%I:%M:%S %p"),
                          "Visited": row[2]} for row in history]
        return history_list
    else:
        raise HTTPException(status_code=404, detail="History list is empty")