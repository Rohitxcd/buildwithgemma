
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
load_dotenv()

from app.api.upload import router as upload_router
from app.api.protect import router as protect_router
from app.api.report import router as report_router

app = FastAPI(
    title="VideoLock API",
    version="1.0.0",
    description="AI-powered preventive media protection platform"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from pathlib import Path
from fastapi.staticfiles import StaticFiles

# Register API routers
app.include_router(upload_router)
app.include_router(protect_router)
app.include_router(report_router)

# Resolve and mount uploads and protected static directories
BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
PROTECTED_DIR = BASE_DIR / "protected"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
PROTECTED_DIR.mkdir(parents=True, exist_ok=True)

app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")
app.mount("/protected", StaticFiles(directory=str(PROTECTED_DIR)), name="protected")

@app.get("/")
async def root():
    return {
        "message": "Welcome to VideoLock API 🚀",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "VideoLock Backend"
    }
