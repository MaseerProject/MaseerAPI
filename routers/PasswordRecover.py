# Import necessary modules and functions
from fastapi import APIRouter, HTTPException
from database import Recover_Password, get_user_by_email
from models import PasswordRecover, Email


# Create an instance of APIRouter
router = APIRouter()



# Define a PUT route for password recovery
@router.put("/RecoverPassword")
async def recoverPassword(passwordRecover: PasswordRecover):
    
    # Call the function to recover password
    Updated = Recover_Password(passwordRecover.email, passwordRecover.password)
    
    # Check if password is updated successfully
    if Updated:
        # If password is updated successfully, return success message
        return {"message": "password updated successfully"}
    else:
        # If user is not found, raise an HTTPException with status code 404 
        raise HTTPException(status_code=404, detail="User_Not_Found")




# Define a POST route to check if email exists for password recovery
@router.post("/EmailRecoverExist")
async def EmailRecoverExist(email: Email):
    # Retrieve user by email from the database
    user = get_user_by_email(email.email)
    
    # Check if user exists
    if user:
        # If user exists, return success message
        return {"message": "Email_Exist"}
    else:
        # If user does not exist, raise an HTTPException with status code 401 
        raise HTTPException(status_code=401, detail="Email_Not_Exist")