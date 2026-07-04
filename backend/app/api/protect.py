import shutil
import uuid
from pathlib import Path

import cv2
from fastapi import APIRouter, File, HTTPException, UploadFile

from app.protection.protection_engine import protection_engine
from app.services.gemma_service import gemma_service
from app.services.report_service import report_service

router = APIRouter(
    prefix="/protect",
    tags=["Protection"],
)

APP_DIR = Path(__file__).resolve().parents[1]
UPLOAD_DIR = APP_DIR / "uploads"
PROTECTED_DIR = APP_DIR / "protected"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
PROTECTED_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/")
async def protect_image(file: UploadFile = File(...)):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Only image files are allowed.",
        )

    file_id = uuid.uuid4().hex
    input_path = UPLOAD_DIR / f"{file_id}.jpg"

    with input_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    image = cv2.imread(str(input_path))

    if image is None:
        raise HTTPException(
            status_code=400,
            detail="Failed to read uploaded image.",
        )

    before_protection = gemma_service.analyze_image(str(input_path))
    strategy = before_protection.get("strategy", {})

    protected_image, protection_metadata = protection_engine.apply(
        image,
        strategy,
    )

    protected_path = PROTECTED_DIR / f"{file_id}.jpg"

    if not cv2.imwrite(str(protected_path), protected_image):
        raise HTTPException(
            status_code=500,
            detail="Failed to save protected image.",
        )

    after_protection = gemma_service.verify_protection(str(protected_path))
    strategy_used = protection_metadata.get("strategy", strategy)

    metadata = {
        "file_id": file_id,
        "original_filename": file.filename,
        "content_type": file.content_type,
        "original_image": str(input_path),
        "faces_detected": protection_metadata.get("faces", 0),
        "image_width": protection_metadata.get("width"),
        "image_height": protection_metadata.get("height"),
        "face_region": protection_metadata.get("region"),
        "operations_applied": protection_metadata.get("operations_applied", []),
    }

    return report_service.generate(
        before_protection=before_protection,
        after_protection=after_protection,
        strategy_used=strategy_used,
        metadata=metadata,
        protected_image=str(protected_path),
    )
