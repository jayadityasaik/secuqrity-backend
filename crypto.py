from Crypto.Cipher import AES
import base64
from config import AES_KEY

def encrypt(data: str):
    cipher = AES.new(AES_KEY, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data.encode())
    return base64.b64encode(cipher.nonce + ciphertext).decode()

def decrypt(enc_data: str):
    raw = base64.b64decode(enc_data)
    nonce = raw[:16]
    ciphertext = raw[16:]
    cipher = AES.new(AES_KEY, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt(ciphertext).decode()