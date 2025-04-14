// Export existing components (leave any existing exports intact)

// Add these new exports for our components:

// Content Management
export { 
    CONTENT_TYPES, 
    AGE_GROUPS, 
    TOPIC_TYPES 
  } from './components/ContentTypes';
  
  export { 
    getContentByType, 
    getContentById 
  } from './components/ContentManager';
  
  // Animation Components
  export { default as AnimationPlayer } from './animated_stories/AnimationPlayer';
  export { 
    safeTouch, 
    getHelpAnimation 
  } from './animated_stories/sampleAnimationData';
  
  // Scenario Components
  export { default as ScenarioSimulation } from './simulations/ScenarioSimulation';
  
  // Language Utilities
  export { 
    setLanguage, 
    getCurrentLanguage, 
    getTranslation, 
    getAllLanguages 
  } from './languages/LanguageManager';
  
  // Test Components
  export { default as TestComponents } from './components/TestComponents';
  