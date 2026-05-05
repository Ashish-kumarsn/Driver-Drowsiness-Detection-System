
// import { Activity } from "lucide-react";

// export const VideoFeed = ({ running }) => {
//   if (!running) return null;
  
//   return (
//     <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
//       <div className="flex items-center gap-2 mb-4">
//         <Activity className="text-green-400 animate-pulse" size={20} />
//         <h3 className="text-xl font-bold text-white">Live Camera Feed</h3>
//       </div>
//       <div className="relative rounded-lg overflow-hidden border-2 border-green-500 shadow-2xl shadow-green-900/30">
//         <img
//           src="http://127.0.0.1:8000/video"
//           alt="Live camera feed"
//           className="w-full h-auto"
//         />
//         <div className="absolute top-4 right-4 bg-red-600 text-white px-3 py-1 rounded-full text-xs font-bold flex items-center gap-1">
//           <div className="w-2 h-2 bg-white rounded-full animate-pulse" />
//           LIVE
//         </div>
//       </div>
//     </div>
//   );
// };














// import { Activity } from "lucide-react";

// export const VideoFeed = ({ running }) => {
//   if (!running) {
//     return (
//       <div className="bg-gray-800 rounded-xl p-4 md:p-6 border border-gray-700 h-full flex items-center justify-center min-h-[300px]">
//         <div className="text-center text-gray-500">
//           <Activity size={48} className="mx-auto mb-3 opacity-30" />
//           <p className="font-medium">Camera feed will appear here</p>
//           <p className="text-sm mt-1">Start detection to begin monitoring</p>
//         </div>
//       </div>
//     );
//   }
  
//   return (
//     <div className="bg-gray-800 rounded-xl p-4 md:p-6 border border-gray-700 sticky top-6">
//       <div className="flex items-center gap-2 mb-4">
//         <Activity className="text-green-400 animate-pulse" size={20} />
//         <h3 className="text-lg md:text-xl font-bold text-white">Live Camera Feed</h3>
//       </div>
//       <div className="relative rounded-lg overflow-hidden border-2 border-green-500 shadow-2xl shadow-green-900/30">
//         <img
//           src="http://127.0.0.1:8000/video"
//           alt="Live camera feed"
//           className="w-full h-auto"
//         />
//         <div className="absolute top-3 right-3 bg-red-600 text-white px-3 py-1 rounded-full text-xs font-bold flex items-center gap-1 shadow-lg">
//           <div className="w-2 h-2 bg-white rounded-full animate-pulse" />
//           LIVE
//         </div>
//       </div>
//     </div>
//   );
// };




import { Activity } from "lucide-react";

export const VideoFeed = ({ running }) => {
  if (!running) {
    return (
      <div className="bg-gray-800 rounded-xl p-4 md:p-6 border border-gray-700 w-full flex items-center justify-center min-h-[400px] lg:min-h-[500px]">
        <div className="text-center text-gray-500">
          <Activity size={48} className="mx-auto mb-3 opacity-30" />
          <p className="font-medium">Camera feed will appear here</p>
          <p className="text-sm mt-1">Start detection to begin monitoring</p>
        </div>
      </div>
    );
  }
  
  return (
    <div className="bg-gray-800 rounded-xl p-4 md:p-6 border border-gray-700 w-full">
      <div className="flex items-center gap-2 mb-4">
        <Activity className="text-green-400 animate-pulse" size={20} />
        <h3 className="text-lg md:text-xl font-bold text-white">Live Camera Feed</h3>
      </div>
      <div className="relative rounded-lg overflow-hidden border-2 border-green-500 shadow-2xl shadow-green-900/30">
        <img
          src="http://127.0.0.1:8000/video"
          alt="Live camera feed"
          className="w-full h-auto"
        />
        <div className="absolute top-3 right-3 bg-red-600 text-white px-3 py-1 rounded-full text-xs font-bold flex items-center gap-1 shadow-lg">
          <div className="w-2 h-2 bg-white rounded-full animate-pulse" />
          LIVE
        </div>
      </div>
    </div>
  );
};