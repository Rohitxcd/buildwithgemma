from typing import Any

import cv2
import numpy as np

from app.protection.blender import blend_face_region
from app.protection.face_mesh import get_face_landmarks
from app.protection.frequency import apply_frequency_perturbation
from app.protection.mask import create_face_mask
from app.protection.roi import extract_face_roi
from app.protection.texture import apply_texture_perturbation

STRENGTH_FACTORS = {
    "low": 0.65,
    "medium": 1.0,
    "high": 1.45,
}


class ProtectionEngine:
    def apply(self, image: np.ndarray, strategy: dict[str, Any]) -> tuple[np.ndarray, dict[str, Any]]:
        normalized_strategy = self._normalize_strategy(strategy)
        strength = normalized_strategy["strength"]
        strength_factor = STRENGTH_FACTORS[strength]

        landmarks = get_face_landmarks(image)

        if not landmarks:
            return image, {
                "faces": 0,
                "width": image.shape[1],
                "height": image.shape[0],
                "region": None,
                "operations_applied": [],
                "strategy": normalized_strategy,
            }

        roi, (x1, y1, x2, y2) = extract_face_roi(
            image,
            landmarks,
        )

        protected_roi = roi.copy()
        operations_applied = []

        if normalized_strategy["landmark_perturbation"]:
            protected_roi = self._apply_landmark_perturbation(
                protected_roi,
                strength_factor,
            )
            operations_applied.append("landmark_perturbation")

        if normalized_strategy["frequency_mask"]:
            frequency_roi = apply_frequency_perturbation(protected_roi)
            alpha = min(1.0, 0.45 * strength_factor)
            protected_roi = cv2.addWeighted(
                frequency_roi,
                alpha,
                protected_roi,
                1.0 - alpha,
                0,
            )
            operations_applied.append("frequency_mask")

        if normalized_strategy["texture_shift"]:
            texture_roi = apply_texture_perturbation(protected_roi)
            alpha = min(1.0, 0.55 * strength_factor)
            protected_roi = cv2.addWeighted(
                texture_roi,
                alpha,
                protected_roi,
                1.0 - alpha,
                0,
            )
            operations_applied.append("texture_shift")

        protected_image = image.copy()
        protected_image[y1:y2, x1:x2] = protected_roi

        mask = create_face_mask(image.shape, landmarks)
        blended = blend_face_region(
            image,
            protected_image,
            mask,
        )

        metadata: dict[str, Any] = {
            "faces": 1,
            "width": image.shape[1],
            "height": image.shape[0],
            "region": [x1, y1, x2, y2],
            "operations_applied": operations_applied,
            "strategy": normalized_strategy,
        }

        return blended, metadata

    def _apply_landmark_perturbation(
        self,
        roi: np.ndarray,
        strength_factor: float,
    ) -> np.ndarray:
        height, width = roi.shape[:2]
        if width < 2 or height < 2:
            return roi

        shift = max(1, int(min(width, height) * 0.018 * strength_factor))

        source = np.float32([
            [0, 0],
            [width - 1, 0],
            [0, height - 1],
        ])
        target = np.float32([
            [shift, 0],
            [width - 1 - shift, shift],
            [0, height - 1 - shift],
        ])

        matrix = cv2.getAffineTransform(source, target)
        warped = cv2.warpAffine(
            roi,
            matrix,
            (width, height),
            flags=cv2.INTER_LINEAR,
            borderMode=cv2.BORDER_REFLECT_101,
        )

        alpha = min(0.85, 0.5 * strength_factor)
        return cv2.addWeighted(warped, alpha, roi, 1.0 - alpha, 0)

    def _normalize_strategy(self, strategy: dict[str, Any] | None) -> dict[str, Any]:
        strategy = strategy or {}
        strength = str(strategy.get("strength", "medium")).lower()
        if strength not in STRENGTH_FACTORS:
            strength = "medium"

        return {
            "landmark_perturbation": bool(strategy.get("landmark_perturbation", True)),
            "frequency_mask": bool(strategy.get("frequency_mask", True)),
            "texture_shift": bool(strategy.get("texture_shift", False)),
            "strength": strength,
        }


protection_engine = ProtectionEngine()
