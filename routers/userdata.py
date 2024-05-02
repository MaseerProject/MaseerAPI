# Import necessary modules and functions
from fastapi import APIRouter, HTTPException
from database import get_userData



# Create an instance of APIRouter
router = APIRouter()

# Define a GET route for retrieving user data by ID
@router.get("/userData/{user_id}")
async def get_user_data(user_id: int):

    # Retrieve user data by user ID
    user_data = get_userData(user_id)
    
    # Check if user data is available
    if user_data:
        # Return user data as a dictionary
        return {
            "name": user_data[0],
            "email": user_data[1],
            "phone_number": user_data[2]    
        }
    else:
        # If user data is not available, raise an HTTPException with status code 404
        raise HTTPException(status_code=404, detail="User_Not_Found")
    
