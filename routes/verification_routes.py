from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from fastapi import Depends

from authenticator_dependency import (
    verify_authenticator_token
)
from database import users_collection

from encryption_service import decrypt_data

from morpho_capture import capture_fingerprint

from authentication_logger import (
    log_authentication
)

router = APIRouter()

# =========================================
# VERIFY REQUEST MODEL
# =========================================

class VerifyIdentity(BaseModel):

    encrypted_qr_data: str

# =========================================
# VERIFY USER IDENTITY
# =========================================

@router.post("/verify")
def verify_identity(
    data: VerifyIdentity,
    auth=Depends(
        verify_authenticator_token
    )
):
    try:

        # =================================
        # DECRYPT QR DATA
        # =================================

        decrypted_data = decrypt_data(
            data.encrypted_qr_data
        )

        # =================================
        # EXTRACT EMAIL
        # =================================

        lines = decrypted_data.split("\n")

        email = None

        for line in lines:

            if "Email:" in line:

                email = line.replace(
                    "Email:",
                    ""
                ).strip()

        if not email:

            raise HTTPException(
                status_code=400,
                detail="Invalid QR Data"
            )

        # =================================
        # FIND USER
        # =================================

        user = users_collection.find_one({

            "email": email

        })

        if not user:

            log_authentication(
                email,
                "FAILED"
            )

            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        # =================================
        # CAPTURE FINGERPRINT
        # =================================

        print(
            "Place finger on scanner..."
        )

        fingerprint_data = (
            capture_fingerprint()
        )

        if not fingerprint_data:

            log_authentication(
                email,
                "FAILED"
            )

            raise HTTPException(
                status_code=401,
                detail="Fingerprint capture failed"
            )

        # =================================
        # LOG SUCCESS
        # =================================

        log_authentication(
            email,
            "SUCCESS"
        )

        return {

            "status":
            "AUTHENTICATION SUCCESSFUL",

            "user":
            user["full_name"],

            "email":
            user["email"]
        }

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)
        )