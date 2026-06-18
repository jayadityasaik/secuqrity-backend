from cryptography.fernet import Fernet

from key_manager import (
    get_active_key,
    get_all_keys
)

# =========================================
# ENCRYPT DATA
# =========================================

def encrypt_data(data: str):

    active_key = get_active_key()

    cipher = Fernet(
        active_key.encode()
    )

    encrypted_data = cipher.encrypt(
        data.encode()
    )

    return encrypted_data.decode()

# =========================================
# DECRYPT DATA
# =========================================

def decrypt_data(encrypted_data: str):

    all_keys = get_all_keys()

    # =====================================
    # TRY ALL KEYS
    # =====================================

    for key in all_keys:

        try:

            cipher = Fernet(
                key.encode()
            )

            decrypted_data = cipher.decrypt(
                encrypted_data.encode()
            )

            return decrypted_data.decode()

        except:

            continue

    # =====================================
    # IF NO KEY WORKS
    # =====================================

    raise Exception(
        "Unable to decrypt QR data"
    )