# Import necessary modules and functions
from fastapi import APIRouter, HTTPException
from models import UserCreate, Email
from database import create_user, check_email



# Create an instance of APIRouter
router = APIRouter()

# Define a POST route for user signup
@router.post("/signup")
async def signup(user_data: UserCreate):
    try:
        # Call the function to create user
        create_user(user_data)  
        return {"message": "Account created successfully"}
    except HTTPException as e:
        return e


# Define a POST route for checking email availability
@router.post("/checkEmail")
async def checkEmail(email: Email):

    # Check if email exists
    new_email = check_email(email.email)
    if new_email:
        return {"message": "The Email is new"}
    else:
        # If email already exists, raise an HTTPException with status code 400 
        raise HTTPException(status_code=400, detail="Email already exists. Please use a different email.")

