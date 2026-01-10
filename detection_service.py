import cv2
import numpy as np
from tensorflow.keras.models import load_model
from collections import deque
import vlc
import time
import threading

# ================== CONFIG ==================

IMG_SIZE = 24
LABELS = ["Closed", "Open"]

CLOSE_PROB_THRESH = 0.6
OPEN_PROB_THRESH = 0.6

BUFFER_SIZE = 7
CLOSED_FRAME_THRESH = 15

MODEL_PATH = "eye_cnn_model.h5"
ALARM_PATH = "focus.mp3"

ALARM_REPEAT_INTERVAL = 3.0

# ================== GLOBAL STATE ==================

model = None
alarm = None
cap = None
running = False
thread = None

eye_state = "OPEN"
closed_counter = 0
last_alarm_time = 0.0
alarm_on = False
eye_buffer = deque(maxlen=BUFFER_SIZE)
latest_frame = None
frame_lock = threading.Lock()


face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
eye_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_eye.xml"
)

# ================== CORE LOOP ==================
def detection_loop():
    global running, eye_state, closed_counter, last_alarm_time, alarm_on, latest_frame

    while running:
        ret, frame = cap.read()
        if not ret:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            # ===== DRAW FACE RECTANGLE =====
            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (255, 0, 0),
                2
            )

            roi_gray = gray[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray)

            predictions = []

            for (ex, ey, ew, eh) in eyes[:2]:
                # ===== DRAW EYE RECTANGLE =====
                cv2.rectangle(
                    frame,
                    (x + ex, y + ey),
                    (x + ex + ew, y + ey + eh),
                    (0, 255, 0),
                    2
                )

                eye_img = roi_gray[ey:ey+eh, ex:ex+ew]
                if eye_img.size == 0:
                    continue

                eye_img = cv2.resize(eye_img, (IMG_SIZE, IMG_SIZE))
                eye_img = eye_img / 255.0
                eye_img = eye_img.reshape(1, IMG_SIZE, IMG_SIZE, 1)

                pred = model.predict(eye_img, verbose=0)[0]
                predictions.append(pred)

            if len(predictions) > 0:
                avg_pred = np.mean(predictions, axis=0)
                eye_buffer.append(avg_pred)

                smooth_pred = np.mean(eye_buffer, axis=0)
                closed_prob, open_prob = smooth_pred

                if closed_prob > CLOSE_PROB_THRESH:
                    closed_counter += 1
                elif open_prob > OPEN_PROB_THRESH:
                    closed_counter = 0
                    eye_state = "OPEN"
                    alarm.stop()
                    alarm_on = False

                if closed_counter >= CLOSED_FRAME_THRESH:
                    eye_state = "CLOSED"
                    now = time.time()
                    if (not alarm_on) or (now - last_alarm_time >= ALARM_REPEAT_INTERVAL):
                        alarm.stop()
                        alarm.play()
                        alarm_on = True
                        last_alarm_time = now

            break  # single face only

        # ===== SAVE FINAL ANNOTATED FRAME FOR STREAM =====
        with frame_lock:
            latest_frame = frame.copy()

# ================== API FUNCTIONS ==================

def start_detection():
    global model, alarm, cap, running, thread

    if running:
        return

    model = load_model(MODEL_PATH)
    alarm = vlc.MediaPlayer(ALARM_PATH)
    cap = cv2.VideoCapture(0)

    running = True
    thread = threading.Thread(target=detection_loop, daemon=True)
    thread.start()

def stop_detection():
    global running, cap

    running = False
    if cap:
        cap.release()

def get_status():
    return {
        "running": running,
        "eye_state": eye_state,
        "closed_frames": closed_counter
    }

def get_frame():
    global latest_frame, running

    if not running or latest_frame is None:
        return None

    with frame_lock:
        ret, buffer = cv2.imencode(".jpg", latest_frame)
        if not ret:
            return None
        return buffer.tobytes()
