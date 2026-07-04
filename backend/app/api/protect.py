import os
import shutil
import uuid
import cv2

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.protection.protection_engine import protection_engine
from app.services.gemma_service import gemma_service
from app.services.report_service import report_service

router = APIRouter(
    prefix="/protect",
    tags=["Protection"]
)

UPLOAD_DIR = "app/uploads"
PROTECTED_DIR = "app/protected"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PROTECTED_DIR, exist_ok=True)


@router.post("/")
async def protect_image(file: UploadFile = File(...)):

    # -----------------------------
    # Validate Upload
    # -----------------------------
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Only image files are allowed."
        )

    # -----------------------------
    # Save Uploaded Image
    # -----------------------------
    file_id = uuid.uuid4().hex

    input_path = os.path.join(
        UPLOAD_DIR,
        f"{file_id}.jpg"
    )

    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # -----------------------------
    # Read Image
    # -----------------------------
    image = cv2.imread(input_path)

    if image is None:
        raise HTTPException(
            status_code=400,
            detail="Failed to read uploaded image."
        )

    # -----------------------------
    # Protection Engine
    # -----------------------------
    protected_image, metadata = protection_engine.apply(image)

    # -----------------------------
    # Save Protected Image
    # -----------------------------
    protected_path = os.path.join(
        PROTECTED_DIR,
        f"{file_id}.jpg"
    )

    cv2.imwrite(
        protected_path,
        protected_image
    )

    metadata["protected_image"] = protected_path
    metadata["original_image"] = input_path

    # -----------------------------
    # Gemma Analysis
    # -----------------------------
    gemma_result = gemma_service.analyze_image(
        metadata
    )

    # -----------------------------
    # Generate Report
    # -----------------------------
    report = report_service.generate(
        metadata,
        gemma_result
    )

    return report