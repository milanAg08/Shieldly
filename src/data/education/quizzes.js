// Mock quiz data - in a real app, this might come from an API or database
const quizzes = {
    en: {
      safetyBasics: {
        id: 'safetyBasics',
        title: 'Safety Quiz',
        questions: [
          {
            id: 1,
            question: 'What should you do if someone touches you in a way that makes you feel uncomfortable?',
            options: [
              'Keep it a secret',
              'Tell a trusted adult',
              'Think it\'s your fault',
              'Do nothing'
            ],
            correctAnswer: 1 // Index of the correct option (Tell a trusted adult)
          },
          {
            id: 2,
            question: 'Which of the following is NOT a safe adult?',
            options: [
              'A teacher at your school',
              'A police officer',
              'Someone who asks you to keep secrets that make you uncomfortable',
              'A school counselor'
            ],
            correctAnswer: 2 // Index of the correct option (Someone who asks you to keep secrets...)
          },
          {
            id: 3,
            question: 'Your body belongs to:',
            options: [
              'Your parents',
              'Your teachers',
              'Adults who take care of you',
              'You'
            ],
            correctAnswer: 3 // Index of the correct option (You)
          },
          {
            id: 4,
            question: 'What are "private parts"?',
            options: [
              'Parts of your body covered by a swimsuit',
              'Your hands and feet',
              'Your face',
              'Your hair'
            ],
            correctAnswer: 0 // Index of the correct option (Parts of your body covered by a swimsuit)
          },
          {
            id: 5,
            question: 'Is it okay for a doctor to look at private parts with a parent present?',
            options: [
              'No, never',
              'Yes, but only if it\'s for your health and a parent is there',
              'Yes, anytime',
              'Only if you\'re not sick'
            ],
            correctAnswer: 1 // Index of the correct option (Yes, but only if it's for your health...)
          }
        ]
      }
    },
    es: {
      safetyBasics: {
        id: 'safetyBasics',
        title: 'Cuestionario de Seguridad',
        questions: [
          {
            id: 1,
            question: '¿Qué debes hacer si alguien te toca de una manera que te hace sentir incómodo?',
            options: [
              'Mantenerlo en secreto',
              'Decírselo a un adulto de confianza',
              'Pensar que es tu culpa',
              'No hacer nada'
            ],
            correctAnswer: 1 // Index of the correct option (Tell a trusted adult)
          },
          {
            id: 2,
            question: '¿Cuál de los siguientes NO es un adulto seguro?',
            options: [
              'Un maestro de tu escuela',
              'Un oficial de policía',
              'Alguien que te pide que guardes secretos que te hacen sentir incómodo',
              'Un consejero escolar'
            ],
            correctAnswer: 2 // Index of the correct option (Someone who asks you to keep secrets...)
          },
          {
            id: 3,
            question: 'Tu cuerpo pertenece a:',
            options: [
              'Tus padres',
              'Tus maestros',
              'Adultos que te cuidan',
              'Ti'
            ],
            correctAnswer: 3 // Index of the correct option (You)
          },
          {
            id: 4,
            question: '¿Qué son las "partes privadas"?',
            options: [
              'Partes de tu cuerpo cubiertas por un traje de baño',
              'Tus manos y pies',
              'Tu cara',
              'Tu pelo'
            ],
            correctAnswer: 0 // Index of the correct option (Parts of your body covered by a swimsuit)
          },
          {
            id: 5,
            question: '¿Está bien que un médico mire las partes privadas con un padre presente?',
            options: [
              'No, nunca',
              'Sí, pero solo si es por tu salud y hay un padre allí',
              'Sí, en cualquier momento',
              'Solo si no estás enfermo'
            ],
            correctAnswer: 1 // Index of the correct option (Yes, but only if it's for your health...)
          }
        ]
      }
    }
  };
  
  // Function to get a quiz by ID and language
  export const getQuiz = (quizId, language = 'en') => {
    // Fallback to English if the requested language is not available
    const lang = quizzes[language] ? language : 'en';
    return quizzes[lang][quizId] || null;
  };
  
  // Function to get all available quiz IDs
  export const getQuizIds = (language = 'en') => {
    const lang = quizzes[language] ? language : 'en';
    return Object.keys(quizzes[lang]);
  };