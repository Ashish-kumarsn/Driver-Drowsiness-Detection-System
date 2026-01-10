import cv2
import numpy as np
from tensorflow.keras.models import load_model

# Load trained model
model = load_model("eye_cnn_model.h5")

# Haar cascades
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
eye_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_eye.xml"
)

IMG_SIZE = 24
LABELS = ["Closed", "Open"]

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        eyes = eye_cascade.detectMultiScale(roi_gray)

        for (ex, ey, ew, eh) in eyes[:2]:
            eye_img = roi_gray[ey:ey+eh, ex:ex+ew]
            eye_img = cv2.resize(eye_img, (IMG_SIZE, IMG_SIZE))
            eye_img = eye_img / 255.0
            eye_img = eye_img.reshape(1, IMG_SIZE, IMG_SIZE, 1)

            prediction = model.predict(eye_img, verbose=0)
            label = LABELS[np.argmax(prediction)]

            cv2.rectangle(
                roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2
            )
            cv2.putText(
                roi_color,
                label,
                (ex, ey-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

    cv2.imshow("Live Eye Detection", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
