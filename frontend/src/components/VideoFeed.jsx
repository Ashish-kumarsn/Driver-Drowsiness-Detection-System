
import { Activity } from "lucide-react";

export const VideoFeed = ({ running }) => {
  if (!running) return null;
  
  return (
    <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
      <div className="flex items-center gap-2 mb-4">
        <Activity className="text-green-400 animate-pulse" size={20} />
        <h3 className="text-xl font-bold text-white">Live Camera Feed</h3>
      </div>
      <div className="relative rounded-lg overflow-hidden border-2 border-green-500 shadow-2xl shadow-green-900/30">
        <img
          src="http://127.0.0.1:8000/video"
          alt="Live camera feed"
          className="w-full h-auto"
        />
        <div className="absolute top-4 right-4 bg-red-600 text-white px-3 py-1 rounded-full text-xs font-bold flex items-center gap-1">
          <div className="w-2 h-2 bg-white rounded-full animate-pulse" />
          LIVE
        </div>
      </div>
    </div>
  );
};