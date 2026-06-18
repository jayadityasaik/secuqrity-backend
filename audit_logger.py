from database import authentication_logs_collection
from datetime import datetime

def log_event(
    event_type: str,
    actor: str,
    status: str,
    details: str = ""
):

    authentication_logs_collection.insert_one({

        "event_type": event_type,

        "actor": actor,

        "status": status,

        "details": details,

        "timestamp": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    })