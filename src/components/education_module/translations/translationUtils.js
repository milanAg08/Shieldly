import React, { createContext, useContext, useState } from 'react';
import enTranslations from './en.json';
import esTranslations from './es.json';

// Create a context for translations
const TranslationContext = createContext();

export const TranslationProvider = ({ children, initialLanguage = 'en' }) => {
  const [language, setLanguage] = useState(initialLanguage);
  
  // Available translations
  const translations = {
    en: enTranslations,
    es: esTranslations
  };
  
  // Get a translation by key path (e.g., "stories.goodBadTouch.title")
  const t = (key) => {
    const keys = key.split('.');
    let value = translations[language];
    
    for (const k of keys) {
      if (!value || !value[k]) {
        console.warn(`Translation key not found: ${key}`);
        return key;
      }
      value = value[k];
    }
    
    return value;
  };
  
  const changeLanguage = (lang) => {
    if (translations[lang]) {
      setLanguage(lang);
    } else {
      console.warn(`Language ${lang} not supported`);
    }
  };
  
  return (
    <TranslationContext.Provider value={{ language, changeLanguage, t }}>
      {children}
    </TranslationContext.Provider>
  );
};

export const useTranslation = () => useContext(TranslationContext);