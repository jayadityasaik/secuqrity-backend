from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

from config import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    QR_SECRET_KEY
)

import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# =====================================
# PASSWORD HASHING
# =====================================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(password, hashed):
    return pwd_context.verify(password, hashed)

# =====================================
# JWT TOKEN
# =====================================

def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({
        "exp": expire
    })

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt

# =====================================
# AES QR ENCRYPTION
# =====================================

AES_KEY = QR_SECRET_KEY.encode('utf-8')

def encrypt_data(data):

    cipher = AES.new(
        AES_KEY.ljust(32, b'0'),
        AES.MODE_CBC
    )

    encrypted = cipher.encrypt(
        pad(data.encode(), AES.block_size)
    )

    return base64.b64encode(
        cipher.iv + encrypted
    ).decode()

def decrypt_data(enc_data):

    raw = base64.b64decode(enc_data)

    iv = raw[:16]

    encrypted = raw[16:]

    cipher = AES.new(
        AES_KEY.ljust(32, b'0'),
        AES.MODE_CBC,
        iv
    )

    decrypted = unpad(
        cipher.decrypt(encrypted),
        AES.block_size
    )

    return decrypted.decode()