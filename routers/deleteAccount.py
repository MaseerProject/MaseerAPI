# Import necessary modules and functions
from fastapi import APIRouter, HTTPException
from database import delete_user_account

router = APIRouter()


# Create an instance of APIRouter
router = APIRouter()  

# Define a DELETE route for deleting a user account
@router.delete("/deleteAccount/{user_id}")  
async def deleteAccount(user_id: int):

    # Call the function to delete the user account
    deleted = delete_user_account(user_id)  
    
    # Check if the user account was successfully deleted
    if deleted:
        # If deleted, return a success message
        return {"message": "User account deleted successfully"}
    else:
        # If not deleted, raise an HTTPException with status code 404
        raise HTTPException(status_code=404, detail="User_Not_Found")