import cv2
import dlib
import numpy as np

RESIZE_HEIGHT = 360

detector = dlib.get_frontal_face_detector()

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        continue
    try:
        det = max(detector(frame), key=lambda r: r.area())
    except Exception as e:
        print(e)
    else:
        cv2.rectangle(
            frame, (det.left(), det.top()), (det.right(), det.bottom()), (0, 0, 255), 2
        )
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, "person", font, 0.5, (255, 255, 255), 1)

    cv2.imshow("detect face 0", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break
