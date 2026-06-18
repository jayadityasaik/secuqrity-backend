from fastapi import Header, HTTPException
from jose import jwt

from config import (
    SECRET_KEY,
    ALGORITHM
)

def verify_admin_token(
    authorization: str = Header(None)
):

    print("AUTH HEADER =", authorization)

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

        print("TOKEN =", token)

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        print("PAYLOAD =", payload)

        role = payload.get("role")

        if role != "admin":

            raise HTTPException(
                status_code=403,
                detail="Admin access required"
            )

        return payload

    except Exception as e:

        print("JWT ERROR =", e)

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )