from fastapi import (
    APIRouter,
    HTTPException,
    Depends
)

from pydantic import BaseModel

from authenticator_dependency import (
    verify_authenticator_token
)

from database import users_collection

from encryption_service import (
    decrypt_data
)

from biometric_matcher import (
    generate_fingerprint_hash
)

from authentication_logger import (
    log_authentication
)

router = APIRouter()

# =========================================
# VERIFY MODEL
# =========================================

class VerifyIdentity(BaseModel):

    encrypted_qr_data: str

    live_fingerprint: str

# =========================================
# VERIFY USER
# =========================================

@router.post("/verify")
def verify_identity(
    data: VerifyIdentity,
    auth=Depends(
        verify_authenticator_token
    )
):

    try:

        decrypted_data = decrypt_data(
            data.encrypted_qr_data
        )

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

        user = users_collection.find_one({

            "email":
            email

        })

        if not user:

            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        live_hash = generate_fingerprint_hash(

            data.live_fingerprint

        )

        if (

            live_hash != user.get(
                "right_thumb_hash"
            )

            and

            live_hash != user.get(
                "left_thumb_hash"
            )

        ):

            log_authentication(
                email,
                "FAILED"
            )

            raise HTTPException(
                status_code=401,
                detail="Fingerprint mismatch"
            )

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