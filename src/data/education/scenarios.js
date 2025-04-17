// Mock scenario data - in a real app, this might come from an API or database
const scenarios = {
    en: {
      safeUnsafe: {
        id: 'safeUnsafe',
        title: 'Safe or Unsafe Touch?',
        description: 'Decide if each situation shows a safe touch or an unsafe touch.',
        messages: {
          correct: 'That\'s right! Good job!',
          incorrect: 'That\'s not quite right. Let\'s try again.',
        },
        items: [
          {
            id: 1,
            image: require('../../assets/images/scenarios/hug_parent.png'),
            text: 'A hug from your parent when you\'re sad',
            correctZone: 'safe',
          },
          {
            id: 2,
            image: require('../../assets/images/scenarios/secret_touch.png'),
            text: 'Someone touching you and asking you to keep it a secret',
            correctZone: 'unsafe',
          },
          {
            id: 3,
            image: require('../../assets/images/scenarios/doctor_exam.png'),
            text: 'A doctor examining you with your parent present',
            correctZone: 'safe',
          },