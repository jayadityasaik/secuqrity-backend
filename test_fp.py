from morpho_capture import capture_fingerprint
from biometric_matcher import generate_fingerprint_hash

print("Capture 1")
fp1 = capture_fingerprint()

print("Capture 2")
fp2 = capture_fingerprint()

print(generate_fingerprint_hash(fp1))
print(generate_fingerprint_hash(fp2))
print(fp1 == fp2)