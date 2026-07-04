import cv2
import numpy as np

from app.protection.face_mesh import get_face_landmarks


class ProtectionEngine:

    def __init__(self):
        pass

    def apply(self, image):

        h, w, _ = image.shape

        landmarks = get_face_landmarks(image)

        if not landmarks:
            return image, {"faces": 0}

        protected = image.copy()

        xs = [p[0] for p in landmarks]
        ys = [p[1] for p in landmarks]

        x1, x2 = max(min(xs)-10, 0), min(max(xs)+10, w)
        y1, y2 = max(min(ys)-10, 0), min(max(ys)+10, h)

        face_roi = protected[y1:y2, x1:x2]

        # ---- Protection Layer 1: subtle blur ----
        face_roi = cv2.GaussianBlur(face_roi, (5, 5), 0)

        # ---- Protection Layer 2: frequency noise ----
        noise = np.random.normal(0, 1.5, face_roi.shape).astype(np.int16)
        face_roi = np.clip(face_roi.astype(np.int16) + noise, 0, 255).astype(np.uint8)

        # ---- Protection Layer 3: mild sharpening ----
        kernel = np.array([[0,-1,0],[-1,5,-1],[0,-1,0]])
        face_roi = cv2.filter2D(face_roi, -1, kernel)

        protected[y1:y2, x1:x2] = face_roi

        metadata = {
            "faces": 1,
            "width": w,
            "height": h,
            "region": [x1, y1, x2, y2]
        }

        return protected, metadata


protection_engine = ProtectionEngine()