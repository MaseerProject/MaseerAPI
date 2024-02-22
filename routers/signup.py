from fastapi import APIRouter, HTTPException
from models import UserCreate
from database import create_user
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import string


router = APIRouter()

@router.post("/signup")
async def signup(user_data: UserCreate):
    try:
        verification_token = ''.join(random.choices(string.ascii_letters + string.digits, k=10))  # Generate verification token
        create_user(user_data, verification_token)  # Pass verification token to create_user function
        # Send verification email
        send_verification_email(user_data.email, verification_token)  # Pass the verification token
        return {"message": "Account created successfully"}
    except HTTPException as e:
        return e





def send_verification_email(email: str, verification_token: str):
    # Set up SMTP server details
    smtp_server = 'smtp.zoho.com'
    smtp_port = 465  # for SSL
    sender_email = 'maseerproject@zohomail.com'
    sender_password = 'Rahaf995500'

    # Create verification link
    verification_link = f"http://127.0.0.1:8000/verify?user_email={email}&token={verification_token}"

    # Create message container
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = 'Verification Email'

    # Compose message
    message = f'''
    Hello,

    Thank you for signing up! Please click the link below to verify your email address:

    {verification_link}

    Regards,
    Maseer App Team
    '''

    msg.attach(MIMEText(message, 'plain'))

    # Connect to SMTP server and send email
    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, msg.as_string())

    print("Verification email sent successfully.")
