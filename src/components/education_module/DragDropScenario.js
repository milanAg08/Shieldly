import React, { useState, useEffect } from 'react';
import { View, Text, Image, TouchableOpacity } from 'react-native';
import { getScenario } from '../../data/education/scenarios';

const DragDropScenario = ({ scenarioId, onComplete, language = 'en' }) => {
  const [scenario, setScenario] = useState(null);
  const [currentItem, setCurrentItem] = useState(0);
  const [score, setScore] = useState(0);
  const [feedback, setFeedback] = useState(null);
  
  useEffect(() => {
    // Load scenario data
    const scenarioData = getScenario(scenarioId, language);
    setScenario(scenarioData);
  }, [scenarioId, language]);
  
  if (!scenario) {
    return <Text>Loading scenario...</Text>;
  }
  
  // In a real implementation, this would use actual drag and drop
  // This simplified version just uses buttons for selection
  const handleSelection = (zone) => {
    const isCorrect = zone === scenario.items[currentItem].correctZone;
    
    // Show feedback
    setFeedback({
      isCorrect,
      message: isCorrect ? scenario.messages.correct : scenario.messages.incorrect
    });
    
    // Update score
    if (isCorrect) {
      setScore(score + 1);
    }
    
    // Move to next item after a delay
    setTimeout(() => {
      setFeedback(null);
      if (currentItem < scenario.items.length - 1) {
        setCurrentItem(currentItem + 1);
      } else {
        // Scenario complete
        onComplete && onComplete(score, scenario.items.length);
      }
    }, 1500);
  };
  
  // If all items have been completed
  if (currentItem >= scenario.items.length) {
    return (
      <View style={styles.container}>
        <Text style={styles.title}>{scenario.title}</Text>
        <Text style={styles.scoreText}>
          Score: {score} / {scenario.items.length}
        </Text>
        <TouchableOpacity 
          style={styles.button} 
          onPress={() => onComplete && onComplete(score, scenario.items.length)}
        >
          <Text style={styles.buttonText}>Continue</Text>
        </TouchableOpacity>
      </View>
    );
  }
  
  const currentScenarioItem = scenario.items[currentItem];
  
  return (
    <View style={styles.container}>
      <Text style={styles.title}>{scenario.title}</Text>
      <Text style={styles.description}>{scenario.description}</Text>
      
      {feedback && (
        <View style={[
          styles.feedbackContainer, 
          { backgroundColor: feedback.isCorrect ? '#d4edda' : '#f8d7da' }
        ]}>
          <Text style={styles.feedbackText}>{feedback.message}</Text>
        </View>
      )}
      
      <View style={styles.itemContainer}>
        <Image 
          source={currentScenarioItem.image} 
          style={styles.itemImage}
          resizeMode="contain"
        />
        <Text style={styles.itemText}>{currentScenarioItem.text}</Text>
      </View>
      
      <View style={styles.choicesContainer}>
        <TouchableOpacity 
          style={[styles.choiceButton, styles.safeButton]} 
          onPress={() => handleSelection('safe')}
        >
          <Text style={styles.buttonText}>Safe</Text>
        </TouchableOpacity>
        <TouchableOpacity 
          style={[styles.choiceButton, styles.unsafeButton]} 
          onPress={() => handleSelection('unsafe')}
        >
          <Text style={styles.buttonText}>Unsafe</Text>
        </TouchableOpacity>
      </View>
      
      <Text style={styles.progressText}>
        {currentItem + 1} / {scenario.items.length}
      </Text>
    </View>
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
  description: {
    fontSize: 16,
    marginBottom: 16,
    textAlign: 'center',
  },
  itemContainer: {
    alignItems: 'center',
    marginVertical: 20,
  },
  itemImage: {
    width: '100%',
    height: 200,
    marginBottom: 12,
  },
  itemText: {
    fontSize: 18,
    textAlign: 'center',
  },
  choicesContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginTop: 24,
  },
  choiceButton: {
    paddingVertical: 12,
    paddingHorizontal: 24,
    borderRadius: 8,
    minWidth: 120,
    alignItems: 'center',
  },
  safeButton: {
    backgroundColor: '#28a745',
  },
  unsafeButton: {
    backgroundColor: '#dc3545',
  },
  buttonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold',
  },
  feedbackContainer: {
    padding: 12,
    borderRadius: 8,
    marginVertical: 16,
  },
  feedbackText: {
    fontSize: 16,
    textAlign: 'center',
  },
  progressText: {
    marginTop: 24,
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
  scoreText: {
    fontSize: 20,
    textAlign: 'center',
    marginVertical: 20,
  },
};

export default DragDropScenario;