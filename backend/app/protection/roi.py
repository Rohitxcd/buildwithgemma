import cv2


def extract_face_roi(image, landmarks, padding=10):
    """
    Extracts the face ROI using landmark coordinates.

    Returns:
        roi
        (x1, y1, x2, y2)
    """

    h, w = image.shape[:2]

    xs = [point[0] for point in landmarks]
    ys = [point[1] for point in landmarks]

    x1 = max(min(xs) - padding, 0)
    y1 = max(min(ys) - padding, 0)

    x2 = min(max(xs) + padding, w)
    y2 = min(max(ys) + padding, h)

    roi = image[y1:y2, x1:x2].copy()

    return roi, (x1, y1, x2, y2)