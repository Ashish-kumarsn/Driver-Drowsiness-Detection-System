import React, { useRef, useEffect } from "react";

const CameraView = () => {
  const videoRef = useRef(null);

  useEffect(() => {
    navigator.mediaDevices
      .getUserMedia({ video: true })
      .then(stream => {
        videoRef.current.srcObject = stream;
      })
      .catch(err => {
        console.error("Camera error:", err);
      });
  }, []);

  return (
    <div>
      <video
        ref={videoRef}
        autoPlay
        playsInline
        width="480"
        height="360"
        style={{ borderRadius: "10px", border: "2px solid #333" }}
      />
    </div>
  );
};

export default CameraView;
