import React, { useState, useEffect } from 'react';
import { View, Text, Image, Button } from 'react-native';
import { getStory } from '../../data/education/stories';

const AnimatedStory = ({ storyId, onComplete, language = 'en' }) => {
  const [currentSlide, setCurrentSlide] = useState(0);
  const [story, setStory] = useState(null);
  
  useEffect(() => {
    // Load story data
    const storyData = getStory(storyId, language);
    setStory(storyData);
  }, [storyId, language]);
  
  if (!story) {
    return <Text>Loading story...</Text>;
  }
  
  const handleNext = () => {
    if (currentSlide < story.slides.length - 1) {
      setCurrentSlide(currentSlide + 1);
    } else {
      onComplete && onComplete();
    }
  };
  
  const handlePrevious = () => {
    if (currentSlide > 0) {
      setCurrentSlide(currentSlide - 1);
    }
  };
  
  return (
    <View style={styles.container}>
      <Text style={styles.title}>{story.title}</Text>
      
      <View style={styles.slideContainer}>
        <Image 
          source={story.slides[currentSlide].image} 
          style={styles.image}
          resizeMode="contain"
        />
        <Text style={styles.slideText}>{story.slides[currentSlide].text}</Text>
      </View>
      
      <View style={styles.navigationContainer}>
        <Button 
          title="Previous" 
          onPress={handlePrevious}
          disabled={currentSlide === 0}
        />
        <Button 
          title={currentSlide < story.slides.length - 1 ? "Next" : "Finish"} 
          onPress={handleNext}
        />
      </View>
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
    marginBottom: 16,
    textAlign: 'center',
  },
  slideContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  image: {
    width: '100%',
    height: 200,
    marginBottom: 16,
  },
  slideText: {
    fontSize: 18,
    textAlign: 'center',
    marginVertical: 16,
  },
  navigationContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: 16,
  },
};

export default AnimatedStory;