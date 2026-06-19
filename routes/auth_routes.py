from audit_logger import log_event

from fastapi import (
    APIRouter,
    HTTPException,
    Depends
)

from pydantic import BaseModel

from datetime import (
    datetime,
    timedelta
)

from database import (
    authenticators_collection,
    users_collection
)

from security import (
    verify_password,
    create_access_token
)

from email_service import (
    generate_otp,
    send_email_otp
)

from authenticator_dependency import (
    verify_authenticator_token
)

from biometric_matcher import (
    generate_fingerprint_hash
)

router = APIRouter()

# =========================================
# TEMP OTP STORAGE
# =========================================

pending_auth_otps = {}

# =========================================
# LOGIN MODEL
# =========================================

class AuthLogin(BaseModel):

    username: str
    password: str

# =========================================
# VERIFY OTP MODEL
# =========================================

class VerifyOTP(BaseModel):

    username: str
    otp: str

# =========================================
# ENROLL USER MODEL
# =========================================

class EnrollUser(BaseModel):

    biometric_token: str

    right_thumb: str

    left_thumb: str

# =========================================
# AUTHENTICATOR LOGIN
# =========================================

@router.post("/login")
def authenticator_login(data: AuthLogin):

    auth = authenticators_collection.find_one({

        "$or": [

            {
                "authenticator_id":
                data.username
            },

            {
                "username":
                data.username
            }
        ]
    })

    if not auth:

        raise HTTPException(
            status_code=404,
            detail="Authenticator not found"
        )

    if not verify_password(
        data.password,
        auth["password"]
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )

    otp = generate_otp()

    pending_auth_otps[
        data.username
    ] = {

        "otp":
        otp,

        "created_at":
        datetime.now()
    }

    send_email_otp(
        auth["email"],
        otp,
        "authenticator"
    )

    return {
        "message":
        "OTP sent to email"
    }

# =========================================
# VERIFY LOGIN OTP
# =========================================

@router.post("/verify-login-otp")
def verify_authenticator_otp(data: VerifyOTP):

    otp_record = pending_auth_otps.get(
        data.username
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

        del pending_auth_otps[
            data.username
        ]

        raise HTTPException(
            status_code=401,
            detail="OTP expired"
        )

    if otp_record["otp"] != data.otp:

        raise HTTPException(
            status_code=400,
            detail="Invalid OTP"
        )

    del pending_auth_otps[
        data.username
    ]

    access_token = create_access_token({

        "sub":
        data.username,

        "role":
        "authenticator"
    })

    log_event(
        "AUTHENTICATOR_LOGIN",
        data.username,
        "SUCCESS"
    )

    return {

        "message":
        "Login successful",

        "access_token":
        access_token
    }

# =========================================
# ENROLL USER
# =========================================

@router.post("/enroll-user")
def enroll_user(
    data: EnrollUser,
    auth=Depends(
        verify_authenticator_token
    )
):

    user = users_collection.find_one({

        "biometric_token":
        data.biometric_token

    })

    if not user:

        raise HTTPException(
            status_code=404,
            detail="Invalid biometric token"
        )

    right_hash = (
        generate_fingerprint_hash(
            data.right_thumb
        )
    )

    left_hash = (
        generate_fingerprint_hash(
            data.left_thumb
        )
    )

    users_collection.update_one(

        {
            "biometric_token":
            data.biometric_token
        },

        {
            "$set": {

                "right_thumb_hash":
                right_hash,

                "left_thumb_hash":
                left_hash,

                "enrolled":
                True
            }
        }
    )

    return {

        "message":
        "User enrolled successfully",

        "user":
        user["full_name"]
    }