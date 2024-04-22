from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from tempfile import NamedTemporaryFile
import shutil
import subprocess

router = APIRouter()



@router.post("/uploadVideo1/{user_id}")
async def uploadVideo(user_id: int, background_tasks: BackgroundTasks, user_video: UploadFile = File(...) ):
    try:
        # Save uploaded video to a temporary file
        with NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
            shutil.copyfileobj(user_video.file, temp_video)
            temp_video_path = temp_video.name
        
        # Process video in the background
        background_tasks.add_task(process_video, user_id, temp_video_path)

        # Return a success message
        return {"message": "Video processing started successfully."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing video: {str(e)}")


def process_video(user_id: str, video_path: str):
    try:
        # Run your YOLO object detection code here
        # Replace this with your YOLO object detection code
        # Use video_path as the input video file

        # For demonstration, let's just copy the input video to the output directory
        output_video_path = f"output_video_{user_id}.mp4"
        shutil.copyfile(video_path, output_video_path)

    except Exception as e:
        print(f"Error processing video for user {user_id}: {str(e)}")