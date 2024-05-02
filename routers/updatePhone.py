# Import necessary modules and functions
from fastapi import APIRouter, HTTPException
from database import update_phone_number
from models import PhoneUpdate


# Create an instance of APIRouter
router = APIRouter()

# Define a PUT route for updating phone number
@router.put("/updatePhone/{user_id}")
async def updatePhone(user_id: int, phone_update: PhoneUpdate):
    
    # Call the function to update phone number
    Updated = update_phone_number(user_id, phone_update.new_phone_number)
    
    # Check if phone number is updated successfully
    if Updated:
        return {"message": "Phone number updated successfully"}
    else:
        # If user not found, raise an HTTPException with status code 404 
        raise HTTPException(status_code=404, detail="User_Not_Found")