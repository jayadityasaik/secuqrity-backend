from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta

from audit_logger import log_event

from database import users_collection

from security import (
    hash_password,
    verify_password
)

from biometric_service import (
    generate_biometric_token
)

from email_service import (
    generate_otp,
    send_email_otp,
    send_user_credentials
)

router = APIRouter()

# =========================================
# TEMP OTP STORAGE
# =========================================

pending_otps = {}

# =========================================
# MODELS
# =========================================

class UserRegister(BaseModel):
    full_name: str
    email: str
    dob: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class VerifyOTP(BaseModel):
    email: str
    otp: str


# =========================================
# REGISTER USER
# =========================================

@router.post("/register")
def register_user(data: UserRegister):

    existing_user = users_collection.find_one({
        "email": data.email
    })

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )

    hashed_password = hash_password(
        data.password
    )

    biometric_token = generate_biometric_token()

    user_document = {

        "full_name":
        data.full_name,

        "email":
        data.email,

        "dob":
        data.dob,

        "password":
        hashed_password,

        "biometric_token":
        biometric_token,

        "right_thumb_hash":
        None,

        "left_thumb_hash":
        None,

        "enrolled":
        False
    }

    users_collection.insert_one(
        user_document
    )

    send_user_credentials(
        data.email,
        data.password,
        biometric_token
    )

    return {

        "message":
        "User registered successfully",

        "biometric_token":
        biometric_token
    }


# =========================================
# USER LOGIN
# =========================================

@router.post("/login")
def login_user(data: UserLogin):

    user = users_collection.find_one({
        "email": data.email
    })

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if not verify_password(
        data.password,
        user["password"]
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )

    otp = generate_otp()

    pending_otps[data.email] = {

        "otp":
        otp,

        "created_at":
        datetime.now()
    }

    send_email_otp(
        data.email,
        otp,
        "user"
    )

    return {

        "message":
        "OTP sent successfully"
    }


# =========================================
# VERIFY OTP
# =========================================

@router.post("/verify-otp")
def verify_otp(data: VerifyOTP):

    otp_record = pending_otps.get(
        data.email
    )

    if not otp_record:

        raise HTTPException(
            status_code=404,
            detail="OTP not found"
        )

    print(
        "Stored OTP:",
        otp_record["otp"]
    )

    print(
        "Entered OTP:",
        data.otp
    )

    print(
        "Created At:",
        otp_record["created_at"]
    )

    print(
        "Current Time:",
        datetime.now()
    )

    print(
        "Expiry Time:",
        otp_record["created_at"]
        + timedelta(minutes=5)
    )

    if datetime.now() >= (

        otp_record["created_at"]
        + timedelta(minutes=5)

    ):

        del pending_otps[
            data.email
        ]

        raise HTTPException(
            status_code=401,
            detail="OTP expired"
        )

    if otp_record["otp"] != data.otp:

        raise HTTPException(
            status_code=401,
            detail="Invalid OTP"
        )

    del pending_otps[
        data.email
    ]

    log_event(
        "USER_LOGIN",
        data.email,
        "SUCCESS"
    )

    return {

        "message":
        "Login successful"
    }
# =========================================
# USER PROFILE
# =========================================

@router.get("/profile/{email}")
def get_user_profile(email: str):

    user = users_collection.find_one(

        {
            "email": email
        },

        {
            "_id": 0,
            "password": 0,
            "right_thumb_hash": 0,
            "left_thumb_hash": 0
        }
    )

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user