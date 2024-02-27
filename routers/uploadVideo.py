from fastapi import APIRouter, File, UploadFile

router = APIRouter()

@router.post("/uploadVideo/")
async def uploadVideo(user_video: UploadFile = File(...)):
    contents = await user_video.read()
    # Save the file or trigger AI processing
    return {"filename": user_video.filename}