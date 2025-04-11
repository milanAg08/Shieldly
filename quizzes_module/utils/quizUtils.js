// Shuffle options randomly
export function shuffleOptions(options) {
    return options.sort(() => Math.random() - 0.5);
  }
  
  // Calculate correct answers
  export function calculateScore(answers) {
    return answers.filter((a) => a.correct).length;
  }
  export function getScorePercentage(answers, totalQuestions) {
    const correct = calculateScore(answers);
    return (correct / totalQuestions) * 100;
  }
  