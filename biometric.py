import hashlib

def extract_features(fingerprint_data: str):
    return hashlib.sha256(fingerprint_data.encode()).hexdigest()

def match(fp1, fp2):
    return fp1 == fp2