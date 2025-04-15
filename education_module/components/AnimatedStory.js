import React, { useState } from 'react';
import { View, Text, Image, TouchableOpacity } from 'react-native';

const AnimatedStory = ({ storyId, onComplete }) => {
  const [currentSlide, setCurrentSlide] = useState(0);
  
  // Mock data - in production this would come from a data file or API
  const stories = {
    goodVsBadTouch: {
      title: "Understanding Touch",
      slides: [
        {
          id: 1,
          image: "placeholder_image_1.png",
          text: "Some touches make us feel safe and loved."
        },
        {
          id: 2,
          image: "placeholder_image_2.png",
          text: "Some touches make us feel uncomfortable or confused."
        },
        {
          id: 3,
          image: "placeholder_image_3.png",
          text: "It's okay to say no to any touch that makes you feel uncomfortable."
        }
      ]
    }
  };
  
  const story = stories[storyId] || stories.goodVsBadTouch;
  
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
    <View>
      <Text>{story.title}</Text>
      <Text>{story.slides[currentSlide].text}</Text>
      <View>
        <TouchableOpacity onPress={handlePrevious} disabled={currentSlide === 0}>
          <Text>Previous</Text>
        </TouchableOpacity>
        <TouchableOpacity onPress={handleNext}>
          <Text>{currentSlide < story.slides.length - 1 ? 'Next' : 'Finish'}</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
};

export default AnimatedStory;