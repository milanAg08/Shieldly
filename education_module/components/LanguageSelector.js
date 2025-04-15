import React from 'react';
import { View, Text, TouchableOpacity } from 'react-native';

const LanguageSelector = ({ currentLanguage, onLanguageChange, availableLanguages = ['en', 'es'] }) => {
  const languageNames = {
    en: 'English',
    es: 'Español',
    fr: 'Français',
    de: 'Deutsch'
  };
  
  return (
    <View style={styles.container}>
      <Text style={styles.label}>Language / Idioma:</Text>
      <View style={styles.buttonContainer}>
        {availableLanguages.map(lang => (
          <TouchableOpacity
            key={lang}
            style={[
              styles.languageButton,
              currentLanguage === lang && styles.activeLanguageButton
            ]}
            onPress={() => onLanguageChange(lang)}
          >
            <Text style={[
              styles.languageText,
              currentLanguage === lang && styles.activeLanguageText
            ]}>
              {languageNames[lang] || lang}
            </Text>
          </TouchableOpacity>
        ))}
      </View>
    </View>
  );
};

const styles = {
  container: {
    padding: 12,
    backgroundColor: '#f8f9fa',
    borderRadius: 8,
  },
  label: {
    fontSize: 14,
    marginBottom: 8,
  },
  buttonContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
  },
  languageButton: {
    paddingVertical: 6,
    paddingHorizontal: 12,
    borderRadius: 16,
    backgroundColor: '#e9ecef',
    marginRight: 8,
    marginBottom: 8,
  },
  activeLanguageButton: {
    backgroundColor: '#007bff',
  },
  languageText: {
    fontSize: 14,
    color: '#495057',
  },
  activeLanguageText: {
    color: 'white',
    fontWeight: 'bold',
  },
};

export default LanguageSelector;