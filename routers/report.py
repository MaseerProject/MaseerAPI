# Import necessary modules and functions
from fastapi import APIRouter, Response, HTTPException
from database import get_report_video, get_report, mark_report_as_visited



# Create an instance of APIRouter
router = APIRouter()



# Define a GET route for retrieving report video
@router.get("/reportvideo/{report_id}")
async def get_video(report_id: int):
    
    # Retrieve video data for the report ID
    video_data = get_report_video(report_id)
    
    # Check if video data is available
    if video_data:
        # Convert bytearray to bytes
        video_data = bytes(video_data)
        # Return video data as a response with media type "video/mp4"
        return Response(content=video_data, media_type="video/mp4")
    else:
        # If video data is not available, return a response with status code 404 (Not Found)
        return Response(status_code=404)




# Define a GET route for retrieving report data
@router.get("/report/{report_id}")
async def getReport(report_id: int):

    # Retrieve report data for the report ID
    report_data = get_report(report_id)
    
    # Check if report data is available
    if report_data:
        # Mark the report as visited
        mark_report_as_visited(report_id)
        
        # Return report data as a dictionary
        return {
            "name": report_data[3],
            "phone_number": report_data[4],
            "violation_type_a_des": report_data[6],
            "violation_date": report_data[8],
            "violation_time": report_data[9],
            "plate_eng_no": report_data[10],
            "plate_arb_no": report_data[11]
        }
    else:
        # If report data is not available, raise an HTTPException with status code 404 (Not Found)
        raise HTTPException(status_code=404, detail="Report_Not_Found")