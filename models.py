from pydantic import BaseModel

# USER REGISTER
class UserRegister(BaseModel):
    name: str
    dob: str
    gender: str
    email: str
    phone: str
    password: str

# USER LOGIN
class UserLogin(BaseModel):
    email: str
    password: str

# OTP VERIFY
class OTPVerify(BaseModel):
    email: str
    otp: str