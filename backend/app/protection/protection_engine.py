import cv2

from app.protection.face_mesh import get_face_landmarks
from app.protection.roi import extract_face_roi
from app.protection.mask import create_face_mask
from app.protection.frequency import apply_frequency_perturbation
from app.protection.texture import apply_texture_perturbation
from app.protection.blender import blend_face_region
from typing import Any


class ProtectionEngine:

    def apply(self, image):

        landmarks = get_face_landmarks(image)

        if not landmarks:
            return image, {
                "faces": 0
            }

        roi, (x1, y1, x2, y2) = extract_face_roi(
            image,
            landmarks
        )

        # Apply transformations
        protected_roi = apply_frequency_perturbation(roi)
        protected_roi = apply_texture_perturbation(protected_roi)

        protected_image = image.copy()
        protected_image[y1:y2, x1:x2] = protected_roi

        # Build full-image mask
        mask = create_face_mask(image.shape, landmarks)

        # Blend
        blended = blend_face_region(
            image,
            protected_image,
            mask
        )

        metadata: dict[str, Any] = {
            "faces": 1,
            "width": image.shape[1],
            "height": image.shape[0],
            "region": [x1, y1, x2, y2]
        }

        return blended, metadata


protection_engine = ProtectionEngine()