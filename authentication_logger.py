from datetime import datetime
from database import authentication_logs_collection

def log_authentication(
    user_email,
    status
):

    authentication_logs_collection.insert_one({

        "user_email": user_email,

        "status": status,

        "timestamp":
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    })