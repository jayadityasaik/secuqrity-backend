from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from routes.setup_routes import router as setup_router
from routes.biometric_routes import router as biometric_router
from routes.qr_routes import router as qr_router
from routes.user_routes import router as user_router
from routes.admin_routes import router as admin_router
from routes.auth_routes import router as auth_router
from routes.scanner_routes import router as scanner_router
from routes.verification_routes import router as verification_router

app = FastAPI()

if not os.path.exists("generated_qr"):
    os.makedirs("generated_qr")

# Serve generated QR PDFs
app.mount(
    "/generated_qr",
    StaticFiles(directory="generated_qr"),
    name="generated_qr"
)
# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://secuqrity-frontend.vercel.app",
        "https://secuqrity-frontend-10djy7dd2-jayadityasaiks-projects.vercel.app",
        "https://secuqrity-frontend-iaezjrct6-jayadityasaiks-projects.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(
    setup_router,
    prefix="/setup",
    tags=["Setup"]
)

app.include_router(
    biometric_router,
    prefix="/biometric",
    tags=["Biometric"]
)

app.include_router(
    verification_router,
    prefix="/verification",
    tags=["Verification"]
)

app.include_router(
    user_router,
    prefix="/user",
    tags=["Users"]
)

app.include_router(
    qr_router,
    prefix="/qr",
    tags=["QR"]
)

app.include_router(
    scanner_router,
    prefix="/scanner",
    tags=["Scanner"]
)

app.include_router(
    admin_router,
    prefix="/admin",
    tags=["Admin"]
)

app.include_router(
    auth_router,
    prefix="/authenticator",
    tags=["Authenticators"]
)

@app.get("/")
def home():
    return {
        "message": "secuQRity Backend Running"
    }
