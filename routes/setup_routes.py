from fastapi import APIRouter
import requests

from database import (
    users_collection,
    authenticators_collection
)

router = APIRouter()

# =========================================
# RD SERVICE STATUS
# =========================================

@router.get("/status")
def check_scanner_status():

    try:

        requests.request(
            "CAPTURE",
            "https://127.0.0.1:11100/capture",
            verify=False,
            timeout=3
        )

        return {
            "rd_service": True,
            "scanner_ready": True,
            "message": "Morpho RD Service Detected"
        }

    except Exception as e:

        return {
            "rd_service": False,
            "scanner_ready": False,
            "message": str(e)
        }

# =========================================
# SCANNER INFORMATION
# =========================================

@router.get("/scanner-info")
def scanner_info():

    return {

        "device_name": "Morpho Fingerprint Scanner",

        "device_type": "L1",

        "modality": "Finger",

        "status": "Connected"
    }

# =========================================
# COMPLETE SYSTEM CHECK
# =========================================

@router.get("/system-check")
def system_check():

    result = {

        "database": False,

        "rd_service": False,

        "scanner_connected": False,

        "authentication_service": True
    }

    try:

        users_collection.count_documents({})
        authenticators_collection.count_documents({})

        result["database"] = True

    except:
        pass

    try:

        requests.request(
            "CAPTURE",
            "https://127.0.0.1:11100/capture",
            verify=False,
            timeout=3
        )

        result["rd_service"] = True
        result["scanner_connected"] = True

    except:
        pass

    result["status"] = (

        "READY"

        if all(result.values())

        else "NOT_READY"
    )

    return result