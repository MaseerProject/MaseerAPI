# Import necessary modules and functions
from fastapi import APIRouter, HTTPException
from database import get_user_by_id, Update_Password
from models import PasswordUpdate

# Create an instance of APIRouter
router = APIRouter()

# Define a PUT route for updating password
@router.put("/updatePassword")
async def updatePassword(passwordUpdate: PasswordUpdate):
    # Retrieve user by ID
    user = get_user_by_id(passwordUpdate.user_id)
    
    # Check if user exists
    if user:
        # Check if old password matches
        if user[1] == passwordUpdate.old_password:
            # If old password matches, update password
            Updated = Update_Password(passwordUpdate.user_id, passwordUpdate.new_password)
            if Updated:
                return {"message": "Password updated successfully"}
            else:
                # If user not found, raise an HTTPException with status code 404
                raise HTTPException(status_code=404, detail="User_Not_Found")
        else:
            # If old password does not match, raise an HTTPException with status code 402 
            raise HTTPException(status_code=402, detail="Password_Not_Match")
    else:
        # If user does not exist, raise an HTTPException with status code 401 
        raise HTTPException(status_code=401, detail="Email_Not_Exist")