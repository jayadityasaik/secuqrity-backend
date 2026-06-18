from fastapi import APIRouter, HTTPException
from morpho_capture import capture_fingerprint

router = APIRouter()

@router.post("/capture")
def capture():

    try:

        fingerprint_data = capture_fingerprint()

        return {
            "success": True,
            "captured": True,
            "length": len(fingerprint_data)
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )