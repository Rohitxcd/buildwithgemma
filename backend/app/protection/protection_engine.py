from typing import Any

import cv2
import numpy as np

from app.protection.body_segmentation import (
    bounding_box_from_mask,
    create_person_mask,
)
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
        protected_image = image.copy()
        operations_applied = []
        face_region = None
        face_mask = np.zeros(image.shape[:2], dtype=np.uint8)
        faces_detected = 0

        if landmarks:
            faces_detected = 1
            roi, (x1, y1, x2, y2) = extract_face_roi(
                image,
                landmarks,
            )
            face_region = [x1, y1, x2, y2]
            protected_roi = self._apply_roi_strategy(
                roi,
                normalized_strategy,
                strength_factor,
                operations_applied,
                "face",
            )
            face_layer = protected_image.copy()
            face_layer[y1:y2, x1:x2] = protected_roi
            face_mask = create_face_mask(image.shape, landmarks)
            protected_image = blend_face_region(
                protected_image,
                face_layer,
                face_mask,
            )

        body_region = None
        body_protected = False

        if normalized_strategy["body_region_protection"]:
            body_mask = create_person_mask(image)
            body_mask = self._remove_face_from_body_mask(body_mask, face_mask)
            body_region = bounding_box_from_mask(body_mask)

            if body_region:
                body_layer = self._apply_body_strategy(
                    protected_image,
                    normalized_strategy,
                    strength_factor,
                    operations_applied,
                )
                protected_image = blend_face_region(
                    protected_image,
                    body_layer,
                    body_mask,
                )
                body_protected = True

        metadata: dict[str, Any] = {
            "faces": faces_detected,
            "width": image.shape[1],
            "height": image.shape[0],
            "region": face_region,
            "face_region": face_region,
            "body_region": body_region,
            "body_protected": body_protected,
            "operations_applied": operations_applied,
            "strategy": normalized_strategy,
        }

        return protected_image, metadata

    def _apply_roi_strategy(
        self,
        roi: np.ndarray,
        strategy: dict[str, Any],
        strength_factor: float,
        operations_applied: list[str],
        prefix: str,
    ) -> np.ndarray:
        protected_roi = roi.copy()

        if strategy["landmark_perturbation"]:
            protected_roi = self._apply_landmark_perturbation(
                protected_roi,
                strength_factor,
            )
            operations_applied.append(f"{prefix}_landmark_perturbation")

        if strategy["frequency_mask"]:
            protected_roi = self._blend_frequency(
                protected_roi,
                strength_factor,
            )
            operations_applied.append(f"{prefix}_frequency_mask")

        if strategy["texture_shift"]:
            protected_roi = self._blend_texture(
                protected_roi,
                strength_factor,
            )
            operations_applied.append(f"{prefix}_texture_shift")

        return protected_roi

    def _apply_body_strategy(
        self,
        image: np.ndarray,
        strategy: dict[str, Any],
        strength_factor: float,
        operations_applied: list[str],
    ) -> np.ndarray:
        protected = image.copy()

        if strategy["frequency_mask"] or not strategy["texture_shift"]:
            protected = self._blend_frequency(
                protected,
                strength_factor,
            )
            operations_applied.append("body_frequency_mask")

        if strategy["texture_shift"]:
            protected = self._blend_texture(
                protected,
                strength_factor,
            )
            operations_applied.append("body_texture_shift")

        return protected

    def _blend_frequency(
        self,
        image: np.ndarray,
        strength_factor: float,
    ) -> np.ndarray:
        frequency_image = apply_frequency_perturbation(image)
        alpha = min(1.0, 0.45 * strength_factor)
        return cv2.addWeighted(
            frequency_image,
            alpha,
            image,
            1.0 - alpha,
            0,
        )

    def _blend_texture(
        self,
        image: np.ndarray,
        strength_factor: float,
    ) -> np.ndarray:
        texture_image = apply_texture_perturbation(image)
        alpha = min(1.0, 0.55 * strength_factor)
        return cv2.addWeighted(
            texture_image,
            alpha,
            image,
            1.0 - alpha,
            0,
        )

    def _remove_face_from_body_mask(
        self,
        body_mask: np.ndarray,
        face_mask: np.ndarray,
    ) -> np.ndarray:
        if not np.any(face_mask):
            return body_mask

        kernel = np.ones((25, 25), dtype=np.uint8)
        expanded_face_mask = cv2.dilate(face_mask, kernel, iterations=1)
        return cv2.bitwise_and(body_mask, cv2.bitwise_not(expanded_face_mask))

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
            "body_region_protection": bool(
                strategy.get("body_region_protection", True)
            ),
            "strength": strength,
        }


protection_engine = ProtectionEngine()
