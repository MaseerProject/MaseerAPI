from fastapi import FastAPI, HTTPException, BackgroundTasks
import asyncio
from models import *
from database import *
from routers import signup, verify, login, userdata, updatePhone, deleteAccount, sendEmail, PasswordRecover, updatePassword, report, historyList, deleteOneReport, deleteUserReports, uploadVideo
app = FastAPI()

app.include_router(signup.router)
app.include_router(verify.router)
app.include_router(login.router)
app.include_router(userdata.router)
app.include_router(updatePhone.router)
app.include_router(deleteAccount.router)
app.include_router(sendEmail.router)
app.include_router(PasswordRecover.router)
app.include_router(updatePassword.router)
app.include_router(report.router)
app.include_router(historyList.router)
app.include_router(deleteOneReport.router)
app.include_router(deleteUserReports.router)
app.include_router(uploadVideo.router)


# Schedule token expiry check to run every 24 hours
TOKEN_EXPIRY_CHECK_INTERVAL = 24 * 60 * 60 # 24 hours in seconds

@app.on_event("startup")
async def startup_event():
    background_tasks = BackgroundTasks()  # Create an instance of BackgroundTasks
    asyncio.create_task(token_expiry_check(background_tasks))  # Pass background_tasks to token_expiry_check

async def token_expiry_check(background_tasks: BackgroundTasks):
    while True:
        background_tasks.add_task(cleanup_expired_tokens)
        await asyncio.sleep(TOKEN_EXPIRY_CHECK_INTERVAL)


    

@app.get("/")
async def root():
    return {"message": "Hello World"}






'''
@app.post("/upload_video")
async def upload_video(user_id: int):
    # Code to handle video upload and storage
    return {"message": "Video uploaded successfully"}


@app.get("/view_reports_list")
async def view_reports_list(user_id: int):
    # Code to retrieve and return a list of reports for the user
    return {"reports": ["Report 1", "Report 2", "Report 3"]}
'''