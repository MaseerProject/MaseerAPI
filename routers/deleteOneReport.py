# Import necessary modules and functions
from fastapi import APIRouter, HTTPException
from database import delete_report


# Create an instance of APIRouter
router = APIRouter()

# Define a DELETE route for deleting a single report
@router.delete("/deleteOneReport/{report_id}")
async def deleteOneReport(report_id: int):
    
    # Call the function to delete the report
    deleted = delete_report(report_id)
    
    # Check if the report was successfully deleted
    if deleted:
        # If deleted, return a success message
        return {"message": "Report deleted successfully"}
    else:
        # If not deleted, raise an HTTPException with status code 404
        raise HTTPException(status_code=404, detail="Report not found")
