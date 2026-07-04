import cv2
import numpy as np


def blend_face_region(original, protected, mask):
    """
    Blend the protected face back into the original image
    using the facial mask.
    """

    mask = cv2.GaussianBlur(mask, (15, 15), 0)

    alpha = mask.astype(np.float32) / 255.0
    alpha = np.expand_dims(alpha, axis=2)

    blended = (
        protected.astype(np.float32) * alpha
        + original.astype(np.float32) * (1 - alpha)
    )

    blended = np.clip(blended, 0, 255).astype(np.uint8)

    return blended