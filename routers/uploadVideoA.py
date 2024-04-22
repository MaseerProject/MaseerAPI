from fastapi import APIRouter, File, UploadFile
import os

router = APIRouter()

@router.post("/uploadVideoAA/")
async def uploadVideo(user_video: UploadFile = File(...)):
    filename, file_extension = os.path.splitext(user_video.filename)
    
    # Check if the file extension indicates it's a video
    video_extensions = ['.mp4', '.mov', '.3gp', '.avi', '.mkv', '.webm', '.wmv', '.flv', '.m4v', '.mpeg']
    if file_extension.lower() not in video_extensions:
        return {"error": "Uploaded file is not a video."}

    contents = await user_video.read()
    # Save the file or trigger AI processing
    return {"filename": user_video.filename}