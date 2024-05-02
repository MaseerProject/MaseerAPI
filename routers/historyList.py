# Import necessary modules and functions
from fastapi import APIRouter, HTTPException
from database import get_user_history


# Create an instance of APIRouter
router = APIRouter()

# Define a GET route for retrieving user history
@router.get("/historyList/{user_id}")
async def historyList(user_id: int):
    # Call the function to retrieve user history
    history = get_user_history(user_id)
    
    # Check if history is not empty
    if history:
        # If history is not empty, format the history data into a list of dictionaries
        history_list = [{"report_id": row[0],
                         "generation_date":  row[1].strftime("%Y-%m-%d"),
                         "generation_day": row[1].strftime("%A"),
                         "generation_time": row[1].strftime("%I:%M:%S %p"),
                         "Visited": row[2]} for row in history]
        return history_list
    else:
        # If history is empty, raise an HTTPException with status code 404
        raise HTTPException(status_code=404, detail="History list is empty")