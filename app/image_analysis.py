import requests

MAX_IMAGE_BYTES = 10 * 1024 * 1024
MAX_WIDTH = 640


def download_image(url: str) -> bytes:
    response = requests.get(
        url, timeout=10, headers={"User-Agent": "Mozilla/5.0"}
    )
    response.raise_for_status()
    if len(response.content) > MAX_IMAGE_BYTES:
        raise ValueError("Zdjęcie jest za duże (limit 10 MB)")
    return response.content


def count_people_in_bytes(image_bytes: bytes) -> int:
    """Zlicza osoby na zdjęciu detektorem HOG z OpenCV."""
    import cv2
    import numpy as np

    image = cv2.imdecode(
        np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR
    )
    if image is None:
        raise ValueError("Nie udało się odczytać zdjęcia")

    height, width = image.shape[:2]
    if width > MAX_WIDTH:
        scale = MAX_WIDTH / width
        image = cv2.resize(image, (MAX_WIDTH, int(height * scale)))

    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    rects, weights = hog.detectMultiScale(
        image, winStride=(4, 4), padding=(8, 8), scale=1.05
    )
    if len(rects) == 0:
        return 0

    boxes = [[int(x), int(y), int(w), int(h)] for x, y, w, h in rects]
    scores = [float(weight) for weight in weights]
    kept = cv2.dnn.NMSBoxes(boxes, scores, 0.3, 0.4)
    return len(kept)


def count_people(url: str) -> int:
    return count_people_in_bytes(download_image(url))
