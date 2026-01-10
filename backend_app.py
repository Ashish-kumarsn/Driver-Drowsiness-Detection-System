from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import time

import detection_service as ds

app = FastAPI(title="Driver Drowsiness Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/start")
def start_detection():
    ds.start_detection()
    return {"status": "started"}

@app.post("/stop")
def stop_detection():
    ds.stop_detection()
    return {"status": "stopped"}

@app.get("/status")
def get_status():
    return ds.get_status()

# ⭐ VIDEO STREAM
def frame_generator():
    while True:
        frame = ds.get_frame()
        if frame is None:
            time.sleep(0.1)
            continue
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" +
            frame +
            b"\r\n"
        )

@app.get("/video")
def video_feed():
    return StreamingResponse(
        frame_generator(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )
