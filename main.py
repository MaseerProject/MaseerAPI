from fastapi import FastAPI, HTTPException, BackgroundTasks
import asyncio
from models import *
from database import *
from routers import signup, verify

app = FastAPI()

app.include_router(signup.router)
app.include_router(verify.router)



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



@app.post("/login")
async def login(credentials: UserCredentials):
    email = credentials.email
    password = credentials.password
    user = get_user_by_email(email)
    if user:
        if user[1] == password:
            return {"message": "Login successful"}
        else:
            raise HTTPException(status_code=401, detail="Invalid password")
    else:
        raise HTTPException(status_code=401, detail="Email does not exist")


'''
@app.get("/get_user_first_name/{user_id}")
async def get_user_first_name_route(user_id: int):
    first_name = get_user_first_name(user_id)
    return {"user_id": user_id, "first_name": first_name}



@app.put("/edit_name")
async def edit_name(user_id: int, new_name: str):
    # Code to update user's name in the database
    return {"message": "Name updated successfully"}

@app.put("/edit_phone_number")
async def edit_phone_number(user_id: int, new_phone_number: str):
    # Code to update user's phone number in the database
    return {"message": "Phone number updated successfully"}

@app.delete("/delete_account")
async def delete_account(user_id: int):
    # Code to delete user's account from the database
    return {"message": "Account deleted successfully"}

@app.post("/upload_video")
async def upload_video(user_id: int):
    # Code to handle video upload and storage
    return {"message": "Video uploaded successfully"}


@app.get("/view_reports_list")
async def view_reports_list(user_id: int):
    # Code to retrieve and return a list of reports for the user
    return {"reports": ["Report 1", "Report 2", "Report 3"]}

@app.get("/view_history_list")
async def view_history_list(user_id: int):
    # Code to retrieve and return a list of user's activity history
    return {"history": ["Activity 1", "Activity 2", "Activity 3"]}

@app.get("/view_report")
async def view_report(report_id: int):
    # Code to retrieve and return details of a specific report
    return {"report": "Report details"}
'''

'''
users = []


# Get all users
@app.get("/userAccounts")
async def get_userAccounts():
    return {"userAccounts": users}

# Get single user
@app.get("/userAccounts/{userID}")
async def get_userAccount(userID: int):
    for user in users:
        if user.Id == userID:
            return {"userAccounts": user}
    return {"massage": "no user found"}


# Create an userAccount
@app.post("/userAccounts")
async def create_userAccounts(user: userAccount):
    users.append(user)
    return {"message": "Account has been created"}


# update userAccount
@app.put("/userAccounts/{userID}")
async def update_userAccount(userID: int, userAcc: userAccount):
    for user in users:
        if user.Id == userID:
            user.Id = userID
            user.name = userAcc.name
            return {"userAccounts": user}
    return {"massage": "no user found"}



# Delete userAccount
@app.delete("/userAccounts/{userID}")
async def Delete_userAccount(userID: int):
    for user in users:
        if user.Id == userID:
            users.remove(user)
            return {"massage": "userAcount deleted"}
    return {"massage": "no user found"}

'''