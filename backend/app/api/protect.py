import os
import shutil
import uuid

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.protection.protection_engine import protection_engine
from app.services.gemma_service import gemma_service
from app.services.report_service import report_service

router = APIRouter(
    prefix="/protect",
    tags=["Protection"]
)

UPLOAD_DIR = "app/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/")
async def protect_image(file: UploadFile = File(...)):

    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Only image files allowed"
        )

    file_id = uuid.uuid4().hex
    input_path = os.path.join(UPLOAD_DIR, f"{file_id}.jpg")

    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # -----------------------------
    # 1. Protection Engine
    # -----------------------------
    protected_image, metadata = protection_engine.apply(input_path)

    # Save protected image
    protected_path = f"app/protected/{file_id}.jpg"
    os.makedirs("app/protected", exist_ok=True)

    import cv2
    cv2.imwrite(protected_path, protected_image)

    metadata["protected_image"] = protected_path

    # -----------------------------
    # 2. Gemma Analysis
    # -----------------------------
    gemma_result = gemma_service.analyze_image(metadata)

    # -----------------------------
    # 3. Final Report
    # -----------------------------
    report = report_service.generate(
        metadata,
        gemma_result
    )

    return report