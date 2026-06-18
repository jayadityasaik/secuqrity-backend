from fastapi import APIRouter
import bcrypt
from database import users

router = APIRouter()

@router.post("/register")
def register(username: str, password: str):
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    users.insert_one({
        "username": username,
        "password": hashed
    })

    return {"msg": "User registered"}

@router.post("/login")
def login(username: str, password: str):
    user = users.find_one({"username": username})

    if not user:
        return {"error": "User not found"}

    if bcrypt.checkpw(password.encode(), user["password"]):
        return {"msg": "Login success"}
    
    return {"error": "Invalid credentials"}