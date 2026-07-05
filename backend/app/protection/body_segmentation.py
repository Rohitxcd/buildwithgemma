import cv2
import mediapipe as mp
import numpy as np

mp_selfie_segmentation = mp.solutions.selfie_segmentation

selfie_segmentation = mp_selfie_segmentation.SelfieSegmentation(
    model_selection=1,
)


def create_person_mask(
    image: np.ndarray,
    threshold: float = 0.25,
) -> np.ndarray:
    """
    Creates a binary person/body mask using MediaPipe Selfie Segmentation.
    """
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = selfie_segmentation.process(rgb)

    if results.segmentation_mask is None:
        return np.zeros(image.shape[:2], dtype=np.uint8)

    mask = (results.segmentation_mask > threshold).astype(np.uint8) * 255

    kernel = np.ones((7, 7), dtype=np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    return mask


def bounding_box_from_mask(mask: np.ndarray) -> list[int] | None:
    points = cv2.findNonZero(mask)
    if points is None:
        return None

    x, y, width, height = cv2.boundingRect(points)
    return [x, y, x + width, y + height]
