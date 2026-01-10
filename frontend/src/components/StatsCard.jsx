export const StatsCard = ({ label, value, status }) => {
  const statusColors = {
    OPEN: 'text-green-400',
    CLOSED: 'text-red-400',
    UNKNOWN: 'text-gray-400',
    active: 'text-blue-400',
    inactive: 'text-gray-400'
  };

  return (
    <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
      <div className="text-gray-400 text-sm font-medium mb-2">{label}</div>
      <div className={`text-2xl font-bold ${statusColors[status] || 'text-white'}`}>
        {value}
      </div>
    </div>
  );
};