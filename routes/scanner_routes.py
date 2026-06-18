from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException,
    Depends
)

import cv2
import numpy as np

from morpho_capture import capture_fingerprint

from authenticator_dependency import (
    verify_authenticator_token
)

router = APIRouter()

# =========================================
# SCAN QR CODE
# =========================================

@router.post("/scan-qr")
async def scan_qr(file: UploadFile = File(...)):

    try:

        image_bytes = await file.read()

        np_array = np.frombuffer(
            image_bytes,
            np.uint8
        )

        image = cv2.imdecode(
            np_array,
            cv2.IMREAD_COLOR
        )

        detector = cv2.QRCodeDetector()

        qr_data, bbox, _ = detector.detectAndDecode(
            image
        )

        if not qr_data:

            raise HTTPException(
                status_code=404,
                detail="No QR code found"
            )

        return {
            "message": "QR scanned successfully",
            "qr_data": qr_data
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# =========================================
# CAPTURE FINGERPRINT
# =========================================

@router.post("/capture-fingerprint")
def capture_fingerprint_route(
    auth=Depends(
        verify_authenticator_token
    )
):

    try:

        fingerprint_data = capture_fingerprint()

        return {

            "success": True,

            "fingerprint_length":
            len(fingerprint_data),

            "fingerprint_data":
            fingerprint_data
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )