import cv2
import math
import numpy as np
import dlib
from imutils import face_utils
import vlc
import webbrowser
from collections import deque

# -------------------- Utility Functions --------------------

def euclideanDist(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

def ear(eye):
    return (
        euclideanDist(eye[1], eye[5]) +
        euclideanDist(eye[2], eye[4])
    ) / (2.0 * euclideanDist(eye[0], eye[3]))

def yawn(mouth):
    return (
        euclideanDist(mouth[2], mouth[10]) +
        euclideanDist(mouth[4], mouth[8])
    ) / (2.0 * euclideanDist(mouth[0], mouth[6]))

def getFaceDirection(shape, size):
    image_points = np.array([
        shape[33], shape[8], shape[45],
        shape[36], shape[54], shape[48]
    ], dtype="double")

    model_points = np.array([
        (0,0,0), (0,-330,-65), (-225,170,-135),
        (225,170,-135), (-150,-150,-125), (150,-150,-125)
    ])

    focal_length = size[1]
    center = (size[1]/2, size[0]/2)
    camera_matrix = np.array([
        [focal_length,0,center[0]],
        [0,focal_length,center[1]],
        [0,0,1]
    ], dtype="double")

    dist = np.zeros((4,1))
    _, _, tvec = cv2.solvePnP(model_points, image_points, camera_matrix, dist)
    return tvec[1][0]

# -------------------- Parameters --------------------

EAR_BUFFER_SIZE = 7
ear_buffer = deque(maxlen=EAR_BUFFER_SIZE)

CLOSE_THRESH = 0.30
OPEN_THRESH  = 0.35

frame_thresh_1 = 15
frame_thresh_2 = 10
frame_thresh_3 = 5

flag = 0
eye_state = "OPEN"
yawn_countdown = 0
map_counter = 0
map_flag = 1

alert = vlc.MediaPlayer('focus.mp3')

# -------------------- Setup --------------------

cap = cv2.VideoCapture(0)
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

(leStart, leEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(reStart, reEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
(mStart, mEnd)   = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]

# -------------------- Main Loop --------------------

while True:
    ret, frame = cap.read()
    if not ret:
        break

    size = frame.shape
    gray = frame
    rects = detector(gray, 0)

    if len(rects):
        shape = face_utils.shape_to_np(predictor(gray, rects[0]))

        leftEye  = shape[leStart:leEnd]
        rightEye = shape[reStart:reEnd]
        mouth    = shape[mStart:mEnd]

        leftEAR  = ear(leftEye)
        rightEAR = ear(rightEye)
        avgEAR   = (leftEAR + rightEAR) / 2.0

        ear_buffer.append(avgEAR)
        smoothEAR = sum(ear_buffer) / len(ear_buffer)

        # ---------------- Eye State Logic ----------------

        if eye_state == "OPEN":
            if smoothEAR < CLOSE_THRESH:
                flag += 1
                if flag >= frame_thresh_3:
                    eye_state = "CLOSED"
        else:
            if smoothEAR > OPEN_THRESH:
                eye_state = "OPEN"
                flag = 0
                alert.stop()
                yawn_countdown = 0
                map_flag = 1

        # ---------------- Yawn Detection ----------------

        if yawn(mouth) > 0.6:
            yawn_countdown = 1
            cv2.putText(frame, "Yawn Detected", (30,40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

        # ---------------- Drowsiness Logic ----------------

        if eye_state == "CLOSED":
            if yawn_countdown and flag >= frame_thresh_3:
                cv2.putText(frame, "Drowsy after Yawn", (30,80),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
                alert.play()
            elif flag >= frame_thresh_2 and getFaceDirection(shape, size) < 0:
                cv2.putText(frame, "Drowsy (Posture)", (30,80),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
                alert.play()
            elif flag >= frame_thresh_1:
                cv2.putText(frame, "Drowsy", (30,80),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
                alert.play()

        # ---------------- Draw & Debug ----------------

        cv2.drawContours(frame, [cv2.convexHull(leftEye)], -1, (0,255,0), 2)
        cv2.drawContours(frame, [cv2.convexHull(rightEye)], -1, (0,255,0), 2)

        cv2.putText(frame,
                    f"EAR:{smoothEAR:.2f} | {eye_state}",
                    (10, size[0]-20),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6, (255,255,255), 2)

    cv2.imshow("Driver", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
