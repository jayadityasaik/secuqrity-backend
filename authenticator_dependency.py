from fastapi import Header, HTTPException
from jose import jwt

from config import (
    SECRET_KEY,
    ALGORITHM
)

def verify_authenticator_token(

    authorization: str = Header(None)

):

    if not authorization:

        raise HTTPException(
            status_code=401,
            detail="Token missing"
        )

    try:

        token = authorization.replace(
            "Bearer ",
            ""
        )

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        role = payload.get("role")

        if role != "authenticator":

            raise HTTPException(
                status_code=403,
                detail="Authenticator access required"
            )

        return payload

    except Exception:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )