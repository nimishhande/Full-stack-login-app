import React from 'react';
import { DivideIcon as LucideIcon } from 'lucide-react';

interface SocialButtonProps {
  provider: string;
  icon: LucideIcon;
  onClick: () => void;
}

const SocialButton: React.FC<SocialButtonProps> = ({ provider, icon: Icon, onClick }) => {
  const providerColors = {
    google: 'hover:bg-red-50 focus:ring-red-500',
    github: 'hover:bg-gray-50 focus:ring-gray-500',
    facebook: 'hover:bg-blue-50 focus:ring-blue-500'
  };

  return (
    <button
      type="button"
      onClick={onClick}
      className={`flex items-center justify-center py-3 px-4 bg-white border border-gray-200 rounded-xl font-medium text-gray-700 transition-all focus:outline-none focus:ring-2 focus:ring-offset-2 ${providerColors[provider as keyof typeof providerColors] || 'hover:bg-gray-50 focus:ring-gray-500'}`}
    >
      <Icon className="w-5 h-5 mr-2" />
      <span className="capitalize">{provider}</span>
    </button>
  );
};

export default SocialButton;