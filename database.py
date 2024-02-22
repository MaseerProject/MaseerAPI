import random
import string
import mysql.connector
from datetime import datetime, timedelta
from fastapi import HTTPException

def connect_to_mysql():
    config = {
        'host': 'bxfb9qeejqcypo9tdkjz-mysql.services.clever-cloud.com',
        'user': 'u4xyd0naitnaz9bu',
        'password': 'Cr4mnlqJ7InUlr55bbm3',
        'database': 'bxfb9qeejqcypo9tdkjz',
    }
    conn = mysql.connector.connect(**config)
    return conn


def get_user_by_email(email):
    conn = connect_to_mysql()
    cursor = conn.cursor()
    query = "SELECT Email, REPLACE (cast(aes_decrypt(`Password`, 'Maseer') as char(100)),`salt`,'') AS Password FROM User_Account WHERE Email = %s"
    cursor.execute(query, (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user




def create_user(user_data, verification_token):
    salt = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    password = user_data.password + salt
    token_expiry = datetime.utcnow() + timedelta(days=1)  # Set token expiry to 24 hours 
    
    conn = connect_to_mysql()
    cursor = conn.cursor()

    # Check if the email already exists
    email_check_query = "SELECT COUNT(*) FROM User_Account WHERE Email = %s"
    cursor.execute(email_check_query, (user_data.email,))
    email_exists = cursor.fetchone()[0]

    if email_exists:
        cursor.close()
        conn.close()
        # If email exists, raise an exception
        raise HTTPException(status_code=400, detail="Email already exists. Please use a different email.")

    # Proceed with inserting the new user if email doesn't exist
    insert_query = "INSERT INTO User_Account (First_Name, Last_Name, Email, Phone_Number, Password, Salt, VerificationToken, TokenExpiry) VALUES (%s, %s, %s, %s, (aes_encrypt(%s,'Maseer')), %s, %s, %s)"
    cursor.execute(insert_query, (user_data.first_name, user_data.last_name, user_data.email, user_data.phone_number, password, salt, verification_token, token_expiry))
    conn.commit()

    cursor.close()
    conn.close()


def verify_user(email: str, token: str) -> str:
    conn = connect_to_mysql()
    cursor = conn.cursor()
    query = "SELECT AccountStatus, TokenExpiry FROM User_Account WHERE Email = %s AND VerificationToken = %s"
    cursor.execute(query, (email, token))
    result = cursor.fetchone()
    if result:
        account_status, token_expiry = result
        # Check if the account is already verified
        if account_status == 1:
            # Account is already verified
            cursor.close()
            conn.close()
            return "This account has already been verified."
        # Check if current timestamp is before the expiry timestamp
        if datetime.utcnow() < token_expiry:
            # Update AccountStatus to 1
            update_query = "UPDATE User_Account SET AccountStatus = 1 WHERE Email = %s"
            cursor.execute(update_query, (email,))
            conn.commit()  # Commit the transaction
            cursor.close()
            conn.close()
            return "Email verification successful."
    cursor.close()
    conn.close()
    # If none of the above conditions are met, return an error message indicating an invalid or expired token
    return "Invalid or expired verification token."


def cleanup_expired_tokens():
    conn = connect_to_mysql()
    cursor = conn.cursor()
    # Query tokens with expiry timestamps older than current time
    query = "DELETE FROM User_Account WHERE AccountStatus = 0 and TokenExpiry < NOW();"
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()


