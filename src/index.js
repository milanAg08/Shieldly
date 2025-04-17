// Export all components from the education module
import { AppRegistry } from 'react-native';
import App from './App';

// Register the app
AppRegistry.registerComponent('HearMe', () => App);

// For web compatibility (if used)
if (module.hot) {
  module.hot.accept();
}

// If you're running in a web environment
if (window) {
  AppRegistry.runApplication('HearMe', {
    rootTag: document.getElementById('root')
  });
}