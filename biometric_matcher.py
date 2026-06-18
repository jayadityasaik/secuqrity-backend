import hashlib

# =========================================
# GENERATE BIOMETRIC HASH
# =========================================

def generate_fingerprint_hash(
    fingerprint_input: str
):

    hashed = hashlib.sha256(

        fingerprint_input.encode()

    ).hexdigest()

    return hashed

# =========================================
# MATCH BIOMETRICS
# =========================================

def match_fingerprint(

    stored_hash: str,
    live_fingerprint: str

):

    live_hash = generate_fingerprint_hash(
        live_fingerprint
    )

    return stored_hash == live_hash