# Import necessary modules and functions
from fastapi import APIRouter, HTTPException
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from models import MailInfo


# Create an instance of APIRouter
router = APIRouter()

# Define a POST route for sending verification email
@router.post("/sendVerificationEmail")
async def sendVerificationEmail(MailInfo:MailInfo):

    try:
        send_verification_email(MailInfo.email, MailInfo.otp_code, 'Email Verification') # Pass the verification token
        return {"message": "verification Email sent successfully"}
    except HTTPException as e:
        return e


# Define a POST route for sending password recovery email
@router.post("/sendPasswordRecoveryEmail")
async def sendPasswordRecoveryEmail(MailInfo:MailInfo):
    try:
        send_verification_email(MailInfo.email, MailInfo.otp_code, 'Password Recovery') # Pass the verification token
        return {"message": "verification Email sent successfully"}
    except HTTPException as e:
        return e

    



# Function to send verification email
def send_verification_email(email: int, otp_code: str, email_Subject: str):
    # Set up SMTP server details
    smtp_server = 'smtp.zoho.com'
    smtp_port = 465  # for SSL
    sender_email = 'maseerproject@zohomail.com'
    sender_password = 'Rahaf995500'



    # Create message container
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = email_Subject

    if email_Subject == 'Email Verification':
        message = f'''
        Hello,

        Thank you for signing up! Please use the following OTP to verify your email address:

        Your OTP for email verification is: {otp_code}

        Regards,
        Maseer App Team
        '''
    elif email_Subject == 'Password Recovery':
        message = f'''
        Hello,

        You have requested to reset your password. Please use the following OTP to proceed:

        Your OTP for password recovery is: {otp_code}

        If you didn't request this, you can safely ignore this email.

        Regards,
        Maseer App Team
        '''

    msg.attach(MIMEText(message, 'plain'))

    # Connect to SMTP server and send email
    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, msg.as_string())

    print("Verification email sent successfully.")
    


