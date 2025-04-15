import React, { createContext, useContext, useState } from 'react';
import enTranslations from '../en.json';
import esTranslations from '../es.json';

const TranslationContext = createContext();

export const TranslationProvider = ({ children }) => {
  const [language, setLanguage] = useState('en');
  
  const translations = {
    en: enTranslations,
    es: esTranslations
  };
  
  const t = (key) => {
    // Simple key path resolver, e.g. 'stories.goodBadTouch.title'
    const keys = key.split('.');
    let value = translations[language];
    
    for (const k of keys) {
      if (!value[k]) return key; // Return the key if translation not found
      value = value[k];
    }
    
    return value;
  };
  
  return (
    <TranslationContext.Provider value={{ language, setLanguage, t }}>
      {children}
    </TranslationContext.Provider>
  );
};

export const useTranslation = () => useContext(TranslationContext);