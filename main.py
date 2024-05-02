# Import necessary modules and functions
from fastapi import FastAPI
from database import connect_to_mysql
from routers import signup, login, userdata, updatePhone, deleteAccount, sendEmail, PasswordRecover, updatePassword, report, historyList, deleteOneReport, uploadVideo

# Create a FastAPI application instance
app = FastAPI()

# Include routers for different endpoints
app.include_router(signup.router)
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
app.include_router(uploadVideo.router)



# Define a root route
@app.get("/")
async def root():
    # Attempt to connect to the MySQL database
    conn = connect_to_mysql()
    
    # Check if the connection was successful
    if conn is not None:
        print("Connection to MySQL database successful")
    else: 
        print("Connection failed")
    
    # Return a response
    return {"message": "Hello World"}

