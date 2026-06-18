from fastapi import APIRouter
import qrcode
from crypto import encrypt, decrypt
from database import biometrics
from biometric import extract_features, match

router = APIRouter()

@router.post("/generate_qr")
def generate_qr(user_id: str, fingerprint: str):
    features = extract_features(fingerprint)

    biometrics.insert_one({
        "user_id": user_id,
        "features": features
    })

    encrypted_data = encrypt(user_id)

    img = qrcode.make(encrypted_data)
    path = f"{user_id}_qr.png"
    img.save(path)

    return {"qr": path}


@router.post("/verify")
def verify(qr_data: str, fingerprint: str):
    user_id = decrypt(qr_data)

    record = biometrics.find_one({"user_id": user_id})
    if not record:
        return {"status": "fail"}

    new_features = extract_features(fingerprint)

    if match(record["features"], new_features):
        return {"status": "authenticated"}
    
    return {"status": "failed"}