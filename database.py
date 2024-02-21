import random
import string
import mysql.connector

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



def create_user(user_data):
    salt = ''.join(random.choices(string.ascii_letters + string.digits, k=8))    
    password = user_data.password + salt
    conn = connect_to_mysql()
    cursor = conn.cursor()
    query = "INSERT INTO User_Account (First_Name, Last_Name, Email, Phone_Number, Password, Salt) VALUES (%s, %s, %s, %s, (aes_encrypt(%s,'Maseer')), %s)"
    cursor.execute(query, (user_data.first_name, user_data.last_name, user_data.email, user_data.phone_number, password, salt))
    conn.commit()
    cursor.close()
    conn.close()





def get_user_first_name(user_id):
    conn = connect_to_mysql()
    cursor = conn.cursor()
    query = "SELECT First_Name FROM User_Account WHERE User_ID = %s"
    cursor.execute(query, (user_id,))
    first_name = cursor.fetchone()[0]  # Assuming First_Name is the first column in the result
    cursor.close()
    conn.close()
    return first_name