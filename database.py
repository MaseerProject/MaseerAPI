import random
import string
import mysql.connector
from datetime import datetime, timedelta
from fastapi import HTTPException

def connect_to_mysql():
    config = {
        'host': 'bi56y3fi8ksmipuyqbbg-mysql.services.clever-cloud.com',
        'user': 'ucp8vo3cbzysdfot',
        'password': '0SYQjw1Iv5VKFbkSyWms',
        'database': 'bi56y3fi8ksmipuyqbbg',
    }
    conn = mysql.connector.connect(**config)
    return conn

#------------------ login ---------------------
def get_user_by_email(email):
    conn = connect_to_mysql()
    cursor = conn.cursor()
    query = "SELECT Email, REPLACE (cast(aes_decrypt(`Password`, 'Maseer') as char(100)),`salt`,'') AS Password, User_ID FROM User_Account WHERE Email = %s"
    cursor.execute(query, (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

#------------------ get_user_by_id ---------------------
def get_user_by_id(user_id):
    conn = connect_to_mysql()
    cursor = conn.cursor()
    query = "SELECT User_ID, REPLACE (cast(aes_decrypt(`Password`, 'Maseer') as char(100)),`salt`,'') AS Password, User_ID FROM User_Account WHERE User_ID = %s"
    cursor.execute(query, (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

# ----------------- userdata --------------------
def get_userData(user_id):
    conn = connect_to_mysql()
    cursor = conn.cursor()
    query = "SELECT CONCAT(First_Name, ' ' , Last_Name) AS Name, Email, Phone_Number FROM User_Account WHERE User_ID = %s"
    cursor.execute(query, (user_id,))
    user_data = cursor.fetchone()
    cursor.close()
    conn.close()
    return user_data


# ----------------- updatePhone --------------------
def update_phone_number(user_id: int, new_phone_number: str) -> bool:
    conn = connect_to_mysql()
    cursor = conn.cursor()
    query = "UPDATE User_Account SET Phone_Number = %s WHERE User_ID = %s"
    cursor.execute(query, (new_phone_number, user_id))
    conn.commit()  # Commit the changes
    rows_affected = cursor.rowcount  # Check the number of rows affected
    cursor.close()
    conn.close()

    # If rows_affected is greater than 0, it means the record has been updated
    return rows_affected > 0


# ----------------- RecoverPassword --------------------
def Recover_Password(email: str, Newpassword: str) -> bool:
    salt = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    password = Newpassword + salt
    conn = connect_to_mysql()
    cursor = conn.cursor()
    query = "UPDATE User_Account SET Password = (aes_encrypt(%s,'Maseer')), salt = %s WHERE Email = %s"
    cursor.execute(query, (password, salt, email))
    conn.commit()  # Commit the changes
    rows_affected = cursor.rowcount  # Check the number of rows affected
    cursor.close()
    conn.close()

    # If rows_affected is greater than 0, it means the record has been updated
    return rows_affected > 0


# ----------------- UpdatePassword --------------------
def Update_Password(user_id: int, Newpassword: str) -> bool:
    salt = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    password = Newpassword + salt
    conn = connect_to_mysql()
    cursor = conn.cursor()
    query = "UPDATE User_Account SET Password = (aes_encrypt(%s,'Maseer')), salt = %s WHERE User_ID = %s"
    cursor.execute(query, (password, salt, user_id))
    conn.commit()  # Commit the changes
    rows_affected = cursor.rowcount  # Check the number of rows affected
    cursor.close()
    conn.close()

    # If rows_affected is greater than 0, it means the record has been updated
    return rows_affected > 0

# ----------------- deleteAccount ---------------------
def delete_user_account(user_id: int) -> bool:
    conn = connect_to_mysql()
    cursor = conn.cursor()
    query = "DELETE FROM User_Account WHERE User_ID = %s"
    cursor.execute(query, (user_id,))
    conn.commit()  # Commit the changes
    rows_affected = cursor.rowcount  # Check the number of rows affected
    cursor.close()
    conn.close()

    # If rows_affected is greater than 0, it means the record has been deleted
    return rows_affected > 0




# ----------------- get_report_video ---------------------
def get_report_video(report_id: int) -> bytearray:
    conn = connect_to_mysql()
    cursor = conn.cursor()

    query = "SELECT (aes_decrypt(`Violation_Video`, 'Maseer')) FROM Reports WHERE Report_ID = %s"
    cursor.execute(query, (report_id,))
    video_data = cursor.fetchone()[0]

    conn.close()

    return video_data

def get_report(report_id: int):
    conn = connect_to_mysql()
    cursor = conn.cursor()
    query = """
        SELECT
            `Report_ID`,
            `User_ID`,
            `Generation_Date`,
            `Name`,
            `Phone_Number`,
            `Violation_Type_ID`,
            `Violation_Type_A_Des`,
            `Violation_Type_E_Des`,
            `Violation_Date`,
            `Violation_Time`,
            `Plate_Eng_No`,
            `Plate_Arb_No`
        FROM
            `Reports_View`
        WHERE
            Report_ID = %s;
    """
    cursor.execute(query, (report_id,))
    report_data = cursor.fetchone()
    cursor.close()
    conn.close()
    return report_data

def mark_report_as_visited(report_id: int):
    conn = connect_to_mysql()
    cursor = conn.cursor()
    try:
        # Update the visited column to 1 for the given report_id
        update_query = "UPDATE Reports_View SET visited = 1 WHERE Report_ID = %s"
        cursor.execute(update_query, (report_id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def mark_report_as_visited(report_id: int) -> bool:
    conn = connect_to_mysql()
    cursor = conn.cursor()
    query = "UPDATE Reports SET visited = 1 WHERE Report_ID = %s"
    cursor.execute(query, (report_id,))
    conn.commit()  # Commit the changes
    rows_affected = cursor.rowcount  # Check the number of rows affected
    cursor.close()
    conn.close()

    # If rows_affected is greater than 0, it means the record has been deleted
    return rows_affected > 0

# ----------------- userHistory ----------------
def get_user_history(user_id: int):
    conn = connect_to_mysql()
    cursor = conn.cursor()
    query = "SELECT `Report_ID`, `Generation_Date` , `Visited` FROM Reports_View WHERE `User_ID` = %s"
    cursor.execute(query, (user_id,))
    history_list = cursor.fetchall()
    cursor.close()
    conn.close()
    return history_list


# ----------------- deleteOneReport ------------
def delete_report(report_id: int) -> bool:
    conn = connect_to_mysql()
    cursor = conn.cursor()
    query = "DELETE FROM Reports WHERE `Report_ID` = %s"
    cursor.execute(query, (report_id,))
    conn.commit()  # Commit the changes
    rows_affected = cursor.rowcount  # Check the number of rows affected
    cursor.close()
    conn.close()

    # If rows_affected is greater than 0, it means the record has been deleted
    return rows_affected > 0

# ----------------- deleteOneReport ------------
def delete_user_reports(user_id: int) -> bool:
    conn = connect_to_mysql()
    cursor = conn.cursor()
    query = "DELETE FROM Reports WHERE `User_ID` = %s"
    cursor.execute(query, (user_id,))
    conn.commit()  # Commit the changes
    rows_affected = cursor.rowcount  # Check the number of rows affected
    cursor.close()
    conn.close()

    # If rows_affected is greater than 0, it means the record has been deleted
    return rows_affected > 0

# ----------------- checkEmail ---------------------
def check_email(email: str) -> bool:
    conn = connect_to_mysql()
    cursor = conn.cursor()

    # Check if the email already exists
    email_check_query = "SELECT COUNT(*) FROM User_Account WHERE Email = %s"
    cursor.execute(email_check_query, (email,))
    email_exists = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return email_exists == 0

# **************************************************************
# ----------------- singup ---------------------
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




