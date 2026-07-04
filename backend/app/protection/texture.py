import cv2
import numpy as np


def apply_texture_perturbation(image):
    """
    Apply subtle texture perturbation.
    """

    noise = np.random.normal(
        0,
        2,
        image.shape
    ).astype(np.float32)

    perturbed = image.astype(np.float32)

    perturbed += noise

    perturbed = np.clip(
        perturbed,
        0,
        255
    )

    perturbed = perturbed.astype(np.uint8)

    return perturbed