import React, { useState, useEffect } from 'react';
import { View, Text, TouchableOpacity, ScrollView } from 'react-native';
import { getQuiz } from '../../data/education/quizzes';

const SafetyQuiz = ({ quizId, onComplete, language = 'en' }) => {
  const [quiz, setQuiz] = useState(null);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState([]);
  const [showResults, setShowResults] = useState(false);
  
  useEffect(() => {
    // Load quiz data
    const quizData = getQuiz(quizId, language);
    setQuiz(quizData);
    
    // Initialize answers array with null values
    if (quizData) {
      setAnswers(new Array(quizData.questions.length).fill(null));
    }
  }, [quizId, language]);
  
  if (!quiz) {
    return <Text>Loading quiz...</Text>;
  }
  
  const handleAnswerSelection = (answerIndex) => {
    const newAnswers = [...answers];
    newAnswers[currentQuestion] = answerIndex;
    setAnswers(newAnswers);
  };
  
  const handleNext = () => {
    if (currentQuestion < quiz.questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
    } else {
      setShowResults(true);
    }
  };
  
  const handlePrevious = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(currentQuestion - 1);
    }
  };
  
  const calculateScore = () => {
    let score = 0;
    answers.forEach((answer, index) => {
      if (answer === quiz.questions[index].correctAnswer) {
        score++;
      }
    });
    return score;
  };
  
  // Display results if quiz is complete
  if (showResults) {
    const score = calculateScore();
    const percentage = Math.round((score / quiz.questions.length) * 100);
    
    return (
      <View style={styles.container}>
        <Text style={styles.title}>{quiz.title} - Results</Text>
        <Text style={styles.scoreText}>
          You scored: {score} out of {quiz.questions.length} ({percentage}%)
        </Text>
        
        <View style={styles.feedbackContainer}>
          <Text style={styles.feedbackTitle}>
            {percentage >= 80 ? "Great job!" : "You can do better!"}
          </Text>
          <Text style={styles.feedbackText}>
            {percentage >= 80 
              ? "You understand safety concepts well!" 
              : "Let's review the safety concepts again."}
          </Text>
        </View>
        
        <TouchableOpacity 
          style={styles.button} 
          onPress={() => onComplete && onComplete(score, quiz.questions.length)}
        >
          <Text style={styles.buttonText}>Continue</Text>
        </TouchableOpacity>
      </View>
    );
  }
  
  const currentQuizQuestion = quiz.questions[currentQuestion];
  
  return (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>{quiz.title}</Text>
      <Text style={styles.progressText}>
        Question {currentQuestion + 1} of {quiz.questions.length}
      </Text>
      
      <View style={styles.questionContainer}>
        <Text style={styles.questionText}>{currentQuizQuestion.question}</Text>
        
        {currentQuizQuestion.options.map((option, index) => (
          <TouchableOpacity 
            key={index}
            style={[
              styles.optionButton,
              answers[currentQuestion] === index && styles.selectedOption
            ]} 
            onPress={() => handleAnswerSelection(index)}
          >
            <Text style={styles.optionText}>{option}</Text>
          </TouchableOpacity>
        ))}
      </View>
      
      <View style={styles.navigationContainer}>
        <TouchableOpacity 
          style={[styles.navButton, currentQuestion === 0 && styles.disabledButton]} 
          onPress={handlePrevious}
          disabled={currentQuestion === 0}
        >
          <Text style={styles.navButtonText}>Previous</Text>
        </TouchableOpacity>
        
        <TouchableOpacity 
          style={[styles.navButton, answers[currentQuestion] === null && styles.disabledButton]} 
          onPress={handleNext}
          disabled={answers[currentQuestion] === null}
        >
          <Text style={styles.navButtonText}>
            {currentQuestion < quiz.questions.length - 1 ? "Next" : "Finish"}
          </Text>
        </TouchableOpacity>
      </View>
    </ScrollView>
  );
};

const styles = {
  container: {
    padding: 16,
    flex: 1,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 8,
    textAlign: 'center',
  },
  progressText: {
    fontSize: 16,
    marginBottom: 20,
    textAlign: 'center',
  },
  questionContainer: {
    marginVertical: 20,
  },
  questionText: {
    fontSize: 18,
    marginBottom: 16,
  },
  optionButton: {
    backgroundColor: '#f8f9fa',
    padding: 16,
    borderRadius: 8,
    marginVertical: 8,
    borderWidth: 1,
    borderColor: '#dee2e6',
  },
  selectedOption: {
    backgroundColor: '#cce5ff',
    borderColor: '#b8daff',
  },
  optionText: {
    fontSize: 16,
  },
  navigationContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: 24,
  },
  navButton: {
    backgroundColor: '#007bff',
    paddingVertical: 12,
    paddingHorizontal: 24,
    borderRadius: 8,
    minWidth: 120,
    alignItems: 'center',
  },
  disabledButton: {
    backgroundColor: '#6c757d',
    opacity: 0.65,
  },
  navButtonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold',
  },
  scoreText: {
    fontSize: 20,
    textAlign: 'center',
    marginVertical: 20,
  },
  feedbackContainer: {
    backgroundColor: '#f8f9fa',
    padding: 16,
    borderRadius: 8,
    marginVertical: 20,
  },
  feedbackTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 8,
    textAlign: 'center',
  },
  feedbackText: {
    fontSize: 16,
    textAlign: 'center',
  },
  button: {
    backgroundColor: '#007bff',
    paddingVertical: 12,
    paddingHorizontal: 24,
    borderRadius: 8,
    alignItems: 'center',
    marginTop: 20,
  },
  buttonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold',
  },
};

export default SafetyQuiz;