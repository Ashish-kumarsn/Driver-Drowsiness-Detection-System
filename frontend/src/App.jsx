/*
import { useState, useEffect } from "react";
import { Activity, Eye, EyeOff, AlertCircle, Power, PowerOff } from "lucide-react";
import {StatusBadge, StatsCard, ErrorAlert, ControlButton, VideoFeed} from './components/index'

export default function App() {
  const [backendOnline, setBackendOnline] = useState(false);
  const [running, setRunning] = useState(false);
  const [eyeState, setEyeState] = useState("UNKNOWN");
  const [closedFrames, setClosedFrames] = useState(0);
  const [error, setError] = useState("");

  const checkHealth = () => fetch("http://127.0.0.1:8000/health").then(r => r.json());
  const startDetection = () => fetch("http://127.0.0.1:8000/start", { method: "POST" });
  const stopDetection = () => fetch("http://127.0.0.1:8000/stop", { method: "POST" });
  const getStatus = () => fetch("http://127.0.0.1:8000/status").then(r => r.json());

  useEffect(() => {
    checkHealth()
      .then(() => setBackendOnline(true))
      .catch(() => setBackendOnline(false));
  }, []);

  useEffect(() => {
    const interval = setInterval(() => {
      getStatus()
        .then((data) => {
          setRunning(data.running);
          setEyeState(data.eye_state);
          setClosedFrames(data.closed_frames);
          setError("");
        })
        .catch(() => {
          setError("Backend not responding");
        });
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  const handleStart = async () => {
    try {
      await startDetection();
      setError("");
    } catch (e) {
      setError("Failed to start detection");
    }
  };

  const handleStop = async () => {
    try {
      await stopDetection();
      setError("");
    } catch (e) {
      setError("Failed to stop detection");
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 p-8">
      <div className="max-w-6xl mx-auto space-y-8">
        
        
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-4xl font-bold text-white mb-2 flex items-center gap-3">
              <Eye className="text-blue-400" size={40} />
              Driver Drowsiness Detection
            </h1>
            <p className="text-gray-400">Real-time monitoring system for driver safety</p>
          </div>
          <StatusBadge online={backendOnline} />
        </div>

        <ErrorAlert message={error} />

        
        <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
          <h2 className="text-xl font-bold text-white mb-4">Control Panel</h2>
          <div className="flex gap-4">
            <ControlButton 
              onClick={handleStart} 
              disabled={!backendOnline || running}
              variant="start"
              icon={Power}
            >
              Start Detection
            </ControlButton>
            <ControlButton 
              onClick={handleStop} 
              disabled={!backendOnline || !running}
              variant="stop"
              icon={PowerOff}
            >
              Stop Detection
            </ControlButton>
          </div>
        </div>

       
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <StatsCard 
            label="System Status" 
            value={running ? "Active" : "Inactive"}
            status={running ? "active" : "inactive"}
          />
          <StatsCard 
            label="Eye State" 
            value={eyeState}
            status={eyeState}
          />
          <StatsCard 
            label="Closed Frame Count" 
            value={closedFrames}
          />
        </div>

        
        <VideoFeed running={running} />

      </div>
    </div>
  );
}

*/
















import { useState, useEffect } from "react";
import { Eye, Power, PowerOff } from "lucide-react";
import {StatusBadge, StatsCard, ErrorAlert, ControlButton, VideoFeed} from './components/index'

export default function App() {
  const [backendOnline, setBackendOnline] = useState(false);
  const [running, setRunning] = useState(false);
  const [eyeState, setEyeState] = useState("UNKNOWN");
  const [closedFrames, setClosedFrames] = useState(0);
  const [error, setError] = useState("");

  const checkHealth = () => fetch("http://127.0.0.1:8000/health").then(r => r.json());
  const startDetection = () => fetch("http://127.0.0.1:8000/start", { method: "POST" });
  const stopDetection = () => fetch("http://127.0.0.1:8000/stop", { method: "POST" });
  const getStatus = () => fetch("http://127.0.0.1:8000/status").then(r => r.json());

  useEffect(() => {
    checkHealth()
      .then(() => setBackendOnline(true))
      .catch(() => setBackendOnline(false));
  }, []);

  useEffect(() => {
    const interval = setInterval(() => {
      getStatus()
        .then((data) => {
          setRunning(data.running);
          setEyeState(data.eye_state);
          setClosedFrames(data.closed_frames);
          setError("");
        })
        .catch(() => {
          setError("Backend not responding");
        });
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  const handleStart = async () => {
    try {
      await startDetection();
      setError("");
    } catch (e) {
      setError("Failed to start detection");
    }
  };

  const handleStop = async () => {
    try {
      await stopDetection();
      setError("");
    } catch (e) {
      setError("Failed to stop detection");
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 p-4 md:p-8">
      <div className="w-auto mx-auto space-y-6">
        
        {/* Header */}
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div>
            <h1 className="text-3xl md:text-4xl font-bold text-white mb-2 flex items-center gap-3">
              <Eye className="text-blue-400" size={36} />
              Driver Drowsiness Detection
            </h1>
            <p className="text-gray-400 text-sm md:text-base">Real-time monitoring system for driver safety</p>
          </div>
          <StatusBadge online={backendOnline} />
        </div>

        {/* Error Alert */}
        <ErrorAlert message={error} />

        {/* Main Content Grid - 2 columns on desktop */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          {/* Left Column - Controls and Stats */}
          <div className="lg:col-span-2 space-y-6">
            
            {/* Control Panel */}
            <div className="bg-gray-800 rounded-xl p-4 md:p-6 border border-gray-700">
              <h2 className="text-lg md:text-xl font-bold text-white mb-4">Control Panel</h2>
              <div className="flex flex-col sm:flex-row gap-3 md:gap-4">
                <ControlButton 
                  onClick={handleStart} 
                  disabled={!backendOnline || running}
                  variant="start"
                  icon={Power}
                >
                  Start Detection
                </ControlButton>
                <ControlButton 
                  onClick={handleStop} 
                  disabled={!backendOnline || !running}
                  variant="stop"
                  icon={PowerOff}
                >
                  Stop Detection
                </ControlButton>
              </div>
            </div>

            {/* Stats Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 md:gap-6">
              <StatsCard 
                label="System Status" 
                value={running ? "Active" : "Inactive"}
                status={running ? "active" : "inactive"}
              />
              <StatsCard 
                label="Eye State" 
                value={eyeState}
                status={eyeState}
              />
              <StatsCard 
                label="Closed Frame Count" 
                value={closedFrames}
              />
            </div>

          </div>

          {/* Right Column - Video Feed */}
          <div className="lg:col-span-1 flex">
            <VideoFeed running={running} />
          </div>

        </div>

      </div>
    </div>
  );
}