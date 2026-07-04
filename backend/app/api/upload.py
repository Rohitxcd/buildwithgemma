from pathlib import Path
import shutil

from fastapi import APIRouter, File, UploadFile, HTTPException

router = APIRouter(prefix="/upload", tags=["Upload"])

UPLOAD_DIR = Path("app/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/")
async def upload_image(file: UploadFile = File(...)):

    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Only image files are allowed."
        )

    destination = UPLOAD_DIR / file.filename

    with destination.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "success": True,
        "filename": file.filename,
        "path": str(destination)
    }