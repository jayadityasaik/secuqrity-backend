from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from audit_logger import log_event

from database import users_collection

from security import verify_password

from encryption_service import encrypt_data

import qrcode
import os

from reportlab.pdfgen import canvas

from PyPDF2 import (
    PdfReader,
    PdfWriter
)

router = APIRouter()

# =========================================
# QR REQUEST MODEL
# =========================================

class GenerateQR(BaseModel):

    email: str
    password: str

# =========================================
# GENERATE USER QR PDF
# =========================================

@router.post("/generate")
def generate_user_qr(data: GenerateQR):

    user = users_collection.find_one({

        "email":
        data.email
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

    # =====================================
    # CHECK ENROLLMENT STATUS
    # =====================================

    if not user.get("enrolled"):

        raise HTTPException(
            status_code=400,
            detail="User biometric enrollment pending"
        )

    # =====================================
    # RAW USER DATA
    # =====================================

    raw_user_data = f"""
Name: {user['full_name']}
Email: {user['email']}
DOB: {user['dob']}
BiometricToken: {user['biometric_token']}
"""

    # =====================================
    # ENCRYPT QR DATA
    # =====================================

    encrypted_qr_data = encrypt_data(
        raw_user_data
    )

    # =====================================
    # CREATE QR FOLDER
    # =====================================

    folder_path = "generated_qr"

    if not os.path.exists(folder_path):

        os.makedirs(folder_path)

    # =====================================
    # QR IMAGE PATH
    # =====================================

    qr_filename = f"{user['email']}.png"

    qr_path = os.path.join(
        folder_path,
        qr_filename
    )

    # =====================================
    # GENERATE QR IMAGE
    # =====================================

    qr_image = qrcode.make(
        encrypted_qr_data
    )

    qr_image.save(qr_path)

    # =====================================
    # CREATE PDF
    # =====================================

    pdf_filename = f"{user['email']}.pdf"

    pdf_path = os.path.join(
        folder_path,
        pdf_filename
    )

    c = canvas.Canvas(
        pdf_path
    )

    c.drawString(
        100,
        800,
        "Secure QR Code"
    )

    c.drawString(
        100,
        780,
        "secuQRity Protected QR"
    )

    c.drawImage(
        qr_path,
        100,
        450,
        width=300,
        height=300
    )

    c.save()

    # =====================================
    # PDF PASSWORD = DOB
    # =====================================

    dob_password = (
        user["dob"]
        .replace("-", "")
        .replace("/", "")
    )

    # =====================================
    # ENCRYPT PDF
    # =====================================

    reader = PdfReader(
        pdf_path
    )

    writer = PdfWriter()

    for page in reader.pages:

        writer.add_page(page)

    writer.encrypt(
        dob_password
    )

    encrypted_pdf_path = os.path.join(
        folder_path,
        f"secured_{pdf_filename}"
    )

    with open(
        encrypted_pdf_path,
        "wb"
    ) as f:

        writer.write(f)

    # =====================================
    # LOG EVENT
    # =====================================

    log_event(
        "QR_GENERATED",
        user["email"],
        "SUCCESS"
    )

    # =====================================
    # RESPONSE
    # =====================================

    return {

        "message":
        "Protected QR PDF generated successfully",

        "pdf_path":
        encrypted_pdf_path,

        "pdf_password":
        dob_password,

        "biometric_token":
        user["biometric_token"],

        "encrypted_qr_data":
        encrypted_qr_data
    }