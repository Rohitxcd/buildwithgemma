import cv2
import numpy as np


def create_face_mask(image_shape, landmarks):
    """
    Creates a binary face mask using a convex hull
    around MediaPipe landmarks.

    Returns:
        mask (uint8)
    """

    mask = np.zeros(image_shape[:2], dtype=np.uint8)

    points = np.array(landmarks, dtype=np.int32)

    hull = cv2.convexHull(points)

    cv2.fillConvexPoly(mask, hull, 255)

    return mask