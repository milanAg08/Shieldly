import React, { useState } from 'react';
import { View, Text, TouchableOpacity } from 'react-native';

const DragDropScenario = ({ scenarioId, onComplete }) => {
  const [currentItem, setCurrentItem] = useState(0);
  const [score, setScore] = useState(0);
  
  // Mock data - in production this would come from a data file or API
  const scenarios = {
    safeUnsafe: {
      title: "Safe or Unsafe Touch?",
      items: [
        {
          id: 1,
          text: "A hug from your parents",
          correctZone: "safe"
        },
        {
          id: 2,
          text: "Someone asking you to keep touching a secret",
          correctZone: "unsafe"
        }
      ]
    }
  };
  
  const scenario = scenarios[scenarioId] || scenarios.safeUnsafe;
  
  // In a real component, this would use proper drag and drop
  // This is just a placeholder for structure
  const handleAnswerSelect = (zone) => {
    const isCorrect = zone === scenario.items[currentItem].correctZone;
    
    if (isCorrect) {
      setScore(score + 1);
    }
    
    if (currentItem < scenario.items.length - 1) {
      setCurrentItem(currentItem + 1);
    } else {
      onComplete && onComplete(score);
    }
  };
  
  if (currentItem >= scenario.items.length) {
    return (
      <View>
        <Text>Scenario Complete!</Text>
        <Text>Your score: {score}/{scenario.items.length}</Text>
        <TouchableOpacity onPress={() => onComplete && onComplete(score)}>
          <Text>Continue</Text>
        </TouchableOpacity>
      </View>
    );
  }
  
  return (
    <View>
      <Text>{scenario.title}</Text>
      <Text>{scenario.items[currentItem].text}</Text>
      <View>
        <TouchableOpacity onPress={() => handleAnswerSelect('safe')}>
          <Text>Safe Touch</Text>
        </TouchableOpacity>
        <TouchableOpacity onPress={() => handleAnswerSelect('unsafe')}>
          <Text>Unsafe Touch</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
};

export default DragDropScenario;