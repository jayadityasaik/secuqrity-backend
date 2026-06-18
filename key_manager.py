import json
import os

from cryptography.fernet import Fernet

# =========================================
# KEY STORAGE FILE
# =========================================

KEY_FILE = "master_key.json"

# =========================================
# INITIALIZE KEY FILE
# =========================================

def initialize_keys():

    if not os.path.exists(KEY_FILE):

        active_key = Fernet.generate_key().decode()

        data = {

            "active_key": active_key,

            "previous_keys": []
        }

        with open(KEY_FILE, "w") as f:

            json.dump(
                data,
                f,
                indent=4
            )

# =========================================
# LOAD KEYS
# =========================================

def load_keys():

    initialize_keys()

    with open(KEY_FILE, "r") as f:

        return json.load(f)

# =========================================
# SAVE KEYS
# =========================================

def save_keys(data):

    with open(KEY_FILE, "w") as f:

        json.dump(
            data,
            f,
            indent=4
        )

# =========================================
# GET ACTIVE KEY
# =========================================

def get_active_key():

    data = load_keys()

    return data["active_key"]

# =========================================
# GET ALL KEYS
# =========================================

def get_all_keys():

    data = load_keys()

    return [

        data["active_key"]

    ] + data["previous_keys"]

# =========================================
# ROTATE KEY
# =========================================

def rotate_key():

    data = load_keys()

    old_key = data["active_key"]

    data["previous_keys"].append(
        old_key
    )

    new_key = Fernet.generate_key().decode()

    data["active_key"] = new_key

    save_keys(data)

    return {

        "message":
        "Encryption key rotated successfully"
    }