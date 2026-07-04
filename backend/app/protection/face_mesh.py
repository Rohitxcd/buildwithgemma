import cv2
import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=True,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5
)


def get_face_landmarks(image):
    """
    Returns 468 face landmarks.
    """

    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    results = face_mesh.process(rgb)

    if not results.multi_face_landmarks:
        return []

    h, w, _ = image.shape

    landmarks = []

    for lm in results.multi_face_landmarks[0].landmark:
        x = int(lm.x * w)
        y = int(lm.y * h)
        landmarks.append((x, y))

    return landmarks