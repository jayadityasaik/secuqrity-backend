from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

DB_NAME = os.getenv("DB_NAME")

SECRET_KEY = os.getenv("SECRET_KEY")

ALGORITHM = os.getenv("ALGORITHM")

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv(
        "ACCESS_TOKEN_EXPIRE_MINUTES",
        "5"
    )
)

QR_SECRET_KEY = os.getenv(
    "QR_SECRET_KEY"
)

EMAIL_ADDRESS = os.getenv(
    "EMAIL_ADDRESS"
)

EMAIL_PASSWORD = os.getenv(
    "EMAIL_PASSWORD"
)