import React from 'react';
import { useLanguage } from '../contexts/LanguageContext';

const LoadingSpinner = ({ size = 'medium' }) => {
  const { t } = useLanguage();
  
  const sizeClasses = {
    small: 'h-4 w-4',
    medium: 'h-6 w-6',
    large: 'h-8 w-8'
  };

  return (
    <div className="flex items-center justify-center space-x-2">
      <div className={`${sizeClasses[size]} animate-spin rounded-full border-2 border-primary border-t-transparent`}></div>
      <span className="text-sm text-gray-600">{t('loading')}</span>
    </div>
  );
};

export default LoadingSpinner;
