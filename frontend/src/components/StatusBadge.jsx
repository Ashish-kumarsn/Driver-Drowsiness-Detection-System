export const StatusBadge = ({ online }) => (
  <div className="flex items-center gap-2 px-4 py-2 rounded-lg bg-gray-800">
    <div className={`w-3 h-3 rounded-full ${online ? 'bg-green-500 animate-pulse' : 'bg-red-500'}`} />
    <span className="text-sm font-medium text-white">
      Backend {online ? 'Online' : 'Offline'}
    </span>
  </div>
);