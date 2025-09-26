import React, { createContext, useContext, useState, useEffect } from 'react';
import { staticTranslations, autoTranslate, autoTranslateMultiple, autoTranslateObject } from '../services/translationService';

const LanguageContext = createContext();

export const useLanguage = () => {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
};

export const LanguageProvider = ({ children }) => {
  const [currentLanguage, setCurrentLanguage] = useState('en');

  // Load saved language from localStorage on component mount
  useEffect(() => {
    const savedLanguage = localStorage.getItem('attensync-language');
    if (savedLanguage && staticTranslations[savedLanguage]) {
      setCurrentLanguage(savedLanguage);
    }
  }, []);

  // Save language to localStorage when it changes
  useEffect(() => {
    localStorage.setItem('attensync-language', currentLanguage);
  }, [currentLanguage]);

  const changeLanguage = (languageCode) => {
    if (staticTranslations[languageCode]) {
      setCurrentLanguage(languageCode);
    }
  };

  // Static translation function (for UI elements)
  const t = (key) => {
    return staticTranslations[currentLanguage]?.[key] || staticTranslations.en[key] || key;
  };

  // Dynamic translation function (for user content like names, messages, etc.)
  const td = async (text) => {
    return await autoTranslate(text, currentLanguage);
  };

  // Translate multiple texts at once
  const tMultiple = async (texts) => {
    return await autoTranslateMultiple(texts, currentLanguage);
  };

  // Translate specific fields in an object (like student data)
  const tObject = async (obj, fieldsToTranslate) => {
    return await autoTranslateObject(obj, fieldsToTranslate, currentLanguage);
  };

  const value = {
    currentLanguage,
    changeLanguage,
    t,           // Static translations (UI elements)
    td,          // Dynamic translations (user content)
    tMultiple,   // Batch translations
    tObject,     // Object field translations
    languages: [
      { code: 'en', name: 'English', nativeName: 'English' },
      { code: 'hi', name: 'Hindi', nativeName: 'हिन्दी' },
      { code: 'pa', name: 'Punjabi', nativeName: 'ਪੰਜਾਬੀ' }
    ]
  };

  return (
    <LanguageContext.Provider value={value}>
      {children}
    </LanguageContext.Provider>
  );
};
