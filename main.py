import cv2
import numpy as np
from tensorflow.keras.models import load_model
from collections import deque
import vlc
import time   # ⭐ ADDED

# ================== CONFIG ==================

IMG_SIZE = 24
LABELS = ["Closed", "Open"]

CLOSE_PROB_THRESH = 0.6        # CNN confidence
OPEN_PROB_THRESH  = 0.6

BUFFER_SIZE = 7               # smoothing window
CLOSED_FRAME_THRESH = 15      # continuous closed frames

MODEL_PATH = "eye_cnn_model.h5"
ALARM_PATH = "focus.mp3"

ALARM_REPEAT_INTERVAL = 3.0   # ⭐ every 3 seconds alarm repeat

# ================== LOAD ==================

model = load_model(MODEL_PATH)
alarm = vlc.MediaPlayer(ALARM_PATH)

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
eye_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_eye.xml"
)

cap = cv2.VideoCapture(0)

# ================== STATE ==================

eye_buffer = deque(maxlen=BUFFER_SIZE)
closed_counter = 0
eye_state = "OPEN"

alarm_on = False                 # ⭐ ADDED
last_alarm_time = 0.0            # ⭐ ADDED

# ================== LOOP ==================

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        eyes = eye_cascade.detectMultiScale(roi_gray)
        predictions = []

        for (ex, ey, ew, eh) in eyes[:2]:
            eye_img = roi_gray[ey:ey+eh, ex:ex+ew]

            if eye_img.size == 0:
                continue

            eye_img = cv2.resize(eye_img, (IMG_SIZE, IMG_SIZE))
            eye_img = eye_img / 255.0
            eye_img = eye_img.reshape(1, IMG_SIZE, IMG_SIZE, 1)

            pred = model.predict(eye_img, verbose=0)[0]
            predictions.append(pred)

            cv2.rectangle(
                roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2
            )

        # ========== DECISION ==========
        if len(predictions) > 0:
            avg_pred = np.mean(predictions, axis=0)
            eye_buffer.append(avg_pred)

            smooth_pred = np.mean(eye_buffer, axis=0)
            closed_prob, open_prob = smooth_pred

            # ---------- CLOSED ----------
            if closed_prob > CLOSE_PROB_THRESH:
                closed_counter += 1

            # ---------- OPEN (RESET) ----------
            elif open_prob > OPEN_PROB_THRESH:
                closed_counter = 0
                eye_state = "OPEN"
                alarm.stop()
                alarm_on = False

            # ---------- DROWSY ----------
            if closed_counter >= CLOSED_FRAME_THRESH:
                eye_state = "CLOSED"
                current_time = time.time()

                # ⭐ AUDIO REPEAT LOGIC (ONLY ADDITION)
                if (not alarm_on) or (current_time - last_alarm_time >= ALARM_REPEAT_INTERVAL):
                    alarm.stop()
                    alarm.play()
                    alarm_on = True
                    last_alarm_time = current_time

            # ========== UI ==========
            status_text = f"{eye_state} | Closed:{closed_prob:.2f}"
            color = (0, 0, 255) if eye_state == "CLOSED" else (0, 255, 0)

            cv2.putText(
                frame, status_text, (30, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2
            )

        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        break  # single face only

    cv2.imshow("Driver Drowsiness Detection", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
