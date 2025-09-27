import React, { useState } from 'react';
import { useLanguage } from '../contexts/LanguageContext';
import { ChevronDown, Languages } from 'lucide-react';

const LanguageSwitcher = () => {
  const { currentLanguage, changeLanguage, languages, t } = useLanguage();
  const [isOpen, setIsOpen] = useState(false);

  const currentLang = languages.find(lang => lang.code === currentLanguage);

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center space-x-2 px-3 py-2 rounded-lg border border-gray-300 hover:border-blue-500 hover:bg-blue-500 hover:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
      >
        <Languages className="h-4 w-4 text-gray-500" />
        <span className="text-sm font-medium text-gray-700">
          {currentLang?.nativeName}
        </span>
        <ChevronDown 
          className={`h-4 w-4 text-gray-500 transform transition-transform ${
            isOpen ? 'rotate-180' : ''
          }`} 
        />
      </button>

      {isOpen && (
        <>
          {/* Backdrop */}
          <div 
            className="fixed inset-0 z-10" 
            onClick={() => setIsOpen(false)}
          />
          
          {/* Dropdown */}
          <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 z-20">
            <div className="py-2">
              <div className="px-3 py-2 text-xs font-semibold text-gray-500 uppercase tracking-wider">
                {t('language')}
              </div>
              {languages.map((language) => (
                <button
                  key={language.code}
                  onClick={() => {
                    changeLanguage(language.code);
                    setIsOpen(false);
                  }}
                  className={`w-full text-left px-3 py-2 text-sm hover:bg-blue-500 hover:text-white flex items-center justify-between ${
                    currentLanguage === language.code 
                      ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-500' 
                      : 'text-gray-700'
                  }`}
                >
                  <div>
                    <div className="font-medium">{language.nativeName}</div>
                    <div className="text-xs text-gray-500">{language.name}</div>
                  </div>
                  {currentLanguage === language.code && (
                    <div className="w-2 h-2 bg-primary-500 rounded-full" />
                  )}
                </button>
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default LanguageSwitcher;
