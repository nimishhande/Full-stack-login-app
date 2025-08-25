import React from 'react';
import { Loader2 } from 'lucide-react';

interface ButtonProps {
  type?: 'button' | 'submit';
  children: React.ReactNode;
  loading?: boolean;
  fullWidth?: boolean;
  variant?: 'primary' | 'secondary';
  onClick?: () => void;
}

const Button: React.FC<ButtonProps> = ({
  type = 'button',
  children,
  loading = false,
  fullWidth = false,
  variant = 'primary',
  onClick
}) => {
  const baseClasses = "flex items-center justify-center py-4 px-6 rounded-xl font-semibold transition-all focus:outline-none focus:ring-2 focus:ring-offset-2";
  const widthClasses = fullWidth ? "w-full" : "";
  
  const variantClasses = {
    primary: "bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500 disabled:bg-blue-400",
    secondary: "bg-gray-100 text-gray-800 hover:bg-gray-200 focus:ring-gray-500 disabled:bg-gray-50"
  };

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={loading}
      className={`${baseClasses} ${widthClasses} ${variantClasses[variant]}`}
    >
      {loading ? (
        <>
          <Loader2 className="w-5 h-5 mr-2 animate-spin" />
          Loading...
        </>
      ) : (
        children
      )}
    </button>
  );
};

export default Button;