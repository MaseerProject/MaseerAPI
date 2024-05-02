# Import necessary modules and functions
from fastapi import APIRouter, HTTPException
from database import get_user_by_email
from models import UserCredentials


# Create an instance of APIRouter
router = APIRouter()

# Define a POST route for user login
@router.post("/login")
async def login(credentials: UserCredentials):
    
    # Extract email and password from the request body
    email = credentials.email
    password = credentials.password
    
    # Retrieve user by email from the database
    user = get_user_by_email(email)
    
    # Check if user exists
    if user:
        # If user exists, check if the password matches
        if user[1] == password:
            # If password matches, return success message with token
            return {"message": "Login_Successful", "token": user[2]}
        else:
            # If password does not match, raise an HTTPException with status code 402 (Payment Required)
            raise HTTPException(status_code=402, detail="Invalid_Password")
    else:
        # If user does not exist, raise an HTTPException with status code 401 (Unauthorized)
        raise HTTPException(status_code=401, detail="Email_Not_Exist")