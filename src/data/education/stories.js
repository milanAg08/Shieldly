// Mock story data - in a real app, this might come from an API or database
const stories = {
    en: {
      goodVsBadTouch: {
        id: 'goodVsBadTouch',
        title: 'Understanding Touch',
        slides: [
          {
            id: 1,
            image: require('../../assets/animations/good_vs_bad_touch/slide1.png'),
            text: 'Some touches make us feel safe and loved, like hugs from family members.',
          },
          {
            id: 2,
            image: require('../../assets/animations/good_vs_bad_touch/slide2.png'),
            text: 'Some touches make us feel uncomfortable or confused. It\'s important to recognize these feelings.',
          },
          {
            id: 3,
            image: require('../../assets/animations/good_vs_bad_touch/slide3.png'),
            text: 'You have the right to say NO to any touch that makes you feel uncomfortable.',
          },
          {
            id: 4,
            image: require('../../assets/animations/good_vs_bad_touch/slide4.png'),
            text: 'If anyone touches you in a way that makes you feel bad, tell a trusted adult right away.',
          },
        ],
      },
      safeAdults: {
        id: 'safeAdults',
        title: 'Safe Adults',
        slides: [
          {
            id: 1,
            image: require('../../assets/animations/safe_adults/slide1.png'),
            text: 'Safe adults are people we can trust to help us when we need it.',
          },
          {
            id: 2,
            image: require('../../assets/animations/safe_adults/slide2.png'),
            text: 'Safe adults listen to our concerns and respect our boundaries.',
          },
          {
            id: 3,
            image: require('../../assets/animations/safe_adults/slide3.png'),
            text: 'Safe adults don\'t ask us to keep secrets that make us feel uncomfortable.',
          },
          {
            id: 4,
            image: require('../../assets/animations/safe_adults/slide4.png'),
            text: 'Examples of safe adults might include parents, teachers, school counselors, and police officers.',
          },
        ],
      },
    },
    es: {
      goodVsBadTouch: {
        id: 'goodVsBadTouch',
        title: 'Entendiendo el Contacto Físico',
        slides: [
          {
            id: 1,
            image: require('../../assets/animations/good_vs_bad_touch/slide1.png'),
            text: 'Algunos contactos nos hacen sentir seguros y queridos, como los abrazos de los miembros de la familia.',
          },
          {
            id: 2,
            image: require('../../assets/animations/good_vs_bad_touch/slide2.png'),
            text: 'Algunos contactos nos hacen sentir incómodos o confundidos. Es importante reconocer estos sentimientos.',
          },
          {
            id: 3,
            image: require('../../assets/animations/good_vs_bad_touch/slide3.png'),
            text: 'Tienes derecho a decir NO a cualquier contacto que te haga sentir incómodo.',
          },
          {
            id: 4,
            image: require('../../assets/animations/good_vs_bad_touch/slide4.png'),
            text: 'Si alguien te toca de una manera que te hace sentir mal, díselo a un adulto de confianza de inmediato.',
          },
        ],
      },
      // More Spanish stories would go here
    },
  };
  
  // Function to get a story by ID and language
  export const getStory = (storyId, language = 'en') => {
    // Fallback to English if the requested language is not available
    const lang = stories[language] ? language : 'en';
    return stories[lang][storyId] || null;
  };
  
  // Function to get all available story IDs
  export const getStoryIds = (language = 'en') => {
    const lang = stories[language] ? language : 'en';
    return Object.keys(stories[lang]);
  };