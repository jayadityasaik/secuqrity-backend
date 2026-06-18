import random
import string

# =========================================
# GENERATE BIOMETRIC TOKEN
# =========================================

def generate_biometric_token():

    characters = (
        string.ascii_uppercase +
        string.digits
    )

    token = "FP-" + ''.join(

        random.choice(characters)

        for _ in range(10)
    )

    return token