import cv2
import numpy as np


def apply_frequency_perturbation(roi):
    """
    Apply subtle frequency-domain perturbation
    while preserving visual quality.
    """

    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    # Fourier Transform
    fft = np.fft.fft2(gray)
    fft_shift = np.fft.fftshift(fft)

    rows, cols = gray.shape
    crow, ccol = rows // 2, cols // 2

    radius = max(5, min(rows, cols) // 20)

    # Create attenuation mask
    y, x = np.ogrid[:rows, :cols]
    mask = ((x - ccol) ** 2 + (y - crow) ** 2) > radius ** 2

    fft_shift = fft_shift * mask

    # Inverse FFT
    fft_inverse = np.fft.ifftshift(fft_shift)
    reconstructed = np.fft.ifft2(fft_inverse)
    reconstructed = np.abs(reconstructed)

    reconstructed = cv2.normalize(
        reconstructed,
        None,
        0,
        255,
        cv2.NORM_MINMAX
    ).astype(np.uint8)

    reconstructed = cv2.cvtColor(
        reconstructed,
        cv2.COLOR_GRAY2BGR
    )

    return reconstructed