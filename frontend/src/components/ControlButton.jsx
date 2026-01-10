export const ControlButton = ({ onClick, disabled, variant, children, icon: Icon }) => {
  const baseStyles = "flex items-center gap-2 px-6 py-3 rounded-lg font-semibold transition-all transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100";
  const variantStyles = variant === 'start' 
    ? 'bg-green-600 hover:bg-green-700 text-white shadow-lg shadow-green-900/50' 
    : 'bg-red-600 hover:bg-red-700 text-white shadow-lg shadow-red-900/50';
  
  return (
    <button 
      onClick={onClick} 
      disabled={disabled}
      className={`${baseStyles} ${variantStyles}`}
    >
      <Icon size={20} />
      {children}
    </button>
  );
};