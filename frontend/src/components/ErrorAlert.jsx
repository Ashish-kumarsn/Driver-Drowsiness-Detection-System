export const ErrorAlert = ({ message }) => {
  if (!message) return null;
  
  return (
    <div className="bg-red-900/30 border border-red-500 rounded-lg p-4 flex items-center gap-3">
      <AlertCircle className="text-red-400 flex-shrink-0" size={24} />
      <span className="text-red-200 font-medium">{message}</span>
    </div>
  );
};