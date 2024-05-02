from pydantic import BaseModel

# Define a Pydantic model for user credentials
class UserCredentials(BaseModel):
    email: str
    password: str

# Define a Pydantic model for creating a new user
class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    password: str

# Define a Pydantic model for updating phone number
class PhoneUpdate(BaseModel):
    new_phone_number: str

# Define a Pydantic model for email information
class MailInfo(BaseModel):
    email: str
    otp_code: str

# Define a Pydantic model for password recovery
class PasswordRecover(BaseModel):
    email: str
    password: str

# Define a Pydantic model for updating password
class PasswordUpdate(BaseModel):
    user_id: int
    old_password: str
    new_password: str

# Define a Pydantic model for email
class Email(BaseModel):
    email: str
