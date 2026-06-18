from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from audit_logger import log_event
from auth_dependency import verify_admin_token

from database import (
    authenticators_collection,
    users_collection,
    authentication_logs_collection
)

from security import (
    hash_password,
    create_access_token
)

from email_service import (
    generate_otp,
    send_email_otp,
    send_authenticator_credentials
)

from key_manager import rotate_key

import random
import string
import csv

from datetime import (
    datetime,
    timedelta
)

from fastapi.responses import (
    FileResponse
)

router = APIRouter()

# =========================================
# ADMIN CREDENTIALS
# =========================================

ADMIN_ID = "biometricQRauthsecurQRity"
ADMIN_PASSWORD = "Authenticity@038"
ADMIN_EMAIL = "cse23733038@matrusri.edu.in"

# =========================================
# TEMP OTP STORAGE
# =========================================

admin_pending_otps = {}

# =========================================
# MODELS
# =========================================

class AdminLogin(BaseModel):

    admin_id: str
    password: str


class VerifyAdminOTP(BaseModel):

    otp: str


class CreateAuthenticator(BaseModel):

    authenticator_name: str
    email: str


# =========================================
# ADMIN LOGIN
# =========================================

@router.post("/login")
def admin_login(data: AdminLogin):

    if data.admin_id != ADMIN_ID:

        raise HTTPException(
            status_code=401,
            detail="Invalid Admin ID"
        )

    if data.password != ADMIN_PASSWORD:

        raise HTTPException(
            status_code=401,
            detail="Invalid Password"
        )

    otp = generate_otp()

    admin_pending_otps["admin"] = {

        "otp":
        otp,

        "created_at":
        datetime.now()
    }

    send_email_otp(
        ADMIN_EMAIL,
        otp,
        "admin"
    )

    return {
        "message":
        "OTP sent to admin email"
    }


# =========================================
# VERIFY ADMIN OTP
# =========================================

@router.post("/verify-login-otp")
def verify_admin_otp(data: VerifyAdminOTP):

    otp_record = admin_pending_otps.get(
        "admin"
    )

    if not otp_record:

        raise HTTPException(
            status_code=404,
            detail="OTP not found"
        )

    if datetime.now() > (

        otp_record["created_at"]
        + timedelta(minutes=5)

    ):

        del admin_pending_otps["admin"]

        raise HTTPException(
            status_code=401,
            detail="OTP expired"
        )

    if otp_record["otp"] != data.otp:

        raise HTTPException(
            status_code=401,
            detail="Invalid OTP"
        )

    del admin_pending_otps["admin"]

    access_token = create_access_token({

        "sub":
        "admin",

        "role":
        "admin"
    })

    log_event(
        "ADMIN_LOGIN",
        "admin",
        "SUCCESS"
    )

    return {

        "message":
        "Admin login successful",

        "access_token":
        access_token
    }


# =========================================
# GENERATE PASSWORD
# =========================================

def generate_random_password():

    chars = (
        string.ascii_letters +
        string.digits
    )

    return "".join(

        random.choice(chars)

        for _ in range(10)
    )


# =========================================
# CREATE AUTHENTICATOR
# =========================================

@router.post("/create-authenticator")
def create_authenticator(
    data: CreateAuthenticator,
    admin=Depends(
        verify_admin_token
    )
):

    existing = authenticators_collection.find_one({

        "email":
        data.email
    })

    if existing:

        raise HTTPException(
            status_code=400,
            detail="Authenticator already exists"
        )

    authenticator_id = (
        "AUTH" +
        str(
            random.randint(
                10000,
                99999
            )
        )
    )

    raw_password = (
        generate_random_password()
    )

    hashed_password = (
        hash_password(
            raw_password
        )
    )

    authenticator_document = {

        "authenticator_id":
        authenticator_id,

        "authenticator_name":
        data.authenticator_name,

        "email":
        data.email,

        "password":
        hashed_password
    }

    authenticators_collection.insert_one(
        authenticator_document
    )

    send_authenticator_credentials(
        data.email,
        authenticator_id,
        raw_password
    )

    return {

        "message":
        "Authenticator created successfully",

        "authenticator_id":
        authenticator_id
    }


@router.get("/all-authenticators")
def get_all_authenticators(
    admin=Depends(
        verify_admin_token
    )
):

    return list(

        authenticators_collection.find(
            {},
            {
                "_id": 0,
                "password": 0
            }
        )
    )


@router.delete(
    "/delete-authenticator/{authenticator_id}"
)
def delete_authenticator(
    authenticator_id: str,
    admin=Depends(
        verify_admin_token
    )
):

    result = authenticators_collection.delete_one({

        "$or": [

            {
                "authenticator_id":
                authenticator_id
            },

            {
                "username":
                authenticator_id
            }
        ]
    })

    if result.deleted_count == 0:

        raise HTTPException(
            status_code=404,
            detail="Authenticator not found"
        )

    return {
        "message":
        "Authenticator deleted successfully"
    }


@router.get("/all-users")
def get_all_users(
    admin=Depends(
        verify_admin_token
    )
):

    return list(

        users_collection.find(
            {},
            {
                "_id": 0,
                "password": 0,
                "right_thumb_hash": 0,
                "left_thumb_hash": 0
            }
        )
    )


@router.delete("/delete-user/{email}")
def delete_user(
    email: str,
    admin=Depends(
        verify_admin_token
    )
):

    result = users_collection.delete_one({
        "email": email
    })

    if result.deleted_count == 0:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "message":
        "User deleted successfully"
    }


@router.post("/rotate-key")
def rotate_encryption_key(
    admin=Depends(
        verify_admin_token
    )
):

    return rotate_key()


@router.get("/authentication-logs")
def get_authentication_logs(
    admin=Depends(
        verify_admin_token
    )
):

    return list(

        authentication_logs_collection.find(
            {},
            {
                "_id": 0
            }
        )
    )


@router.get("/system-stats")
def get_system_stats(
    admin=Depends(
        verify_admin_token
    )
):

    total_users = (
        users_collection.count_documents({})
    )

    total_authenticators = (
        authenticators_collection.count_documents({})
    )

    enrolled_users = (
        users_collection.count_documents({
            "enrolled": True
        })
    )

    pending_users = (
        users_collection.count_documents({
            "$or": [
                {
                    "enrolled": False
                },
                {
                    "enrolled": {
                        "$exists": False
                    }
                }
            ]
        })
    )

    total_verifications = (
        authentication_logs_collection.count_documents({})
    )

    return {

        "total_users":
        total_users,

        "total_authenticators":
        total_authenticators,

        "enrolled_users":
        enrolled_users,

        "pending_users":
        pending_users,

        "total_verifications":
        total_verifications
    }


@router.get("/export-logs")
def export_logs(
    admin=Depends(
        verify_admin_token
    )
):

    csv_file = "authentication_logs.csv"

    logs = list(
        authentication_logs_collection.find(
            {},
            {
                "_id": 0
            }
        )
    )

    with open(
        csv_file,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "user_email",
            "status",
            "timestamp"
        ])

        for log in logs:

            writer.writerow([

                log.get(
                    "user_email",
                    ""
                ),

                log.get(
                    "status",
                    ""
                ),

                log.get(
                    "timestamp",
                    ""
                )
            ])

    return FileResponse(

        path=csv_file,

        filename=
        "authentication_logs.csv",

        media_type=
        "text/csv"
    )
