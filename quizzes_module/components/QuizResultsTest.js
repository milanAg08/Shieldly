import React from "react";

export default function QuizResultsTest({ results }) {
  // Calculate the score
  const correctAnswers = results.filter(answer => answer.correct).length;
  const totalQuestions = results.length;
  const scorePercentage = Math.round((correctAnswers / totalQuestions) * 100);
  
  // Determine performance level
  const getPerformanceText = () => {
    if (scorePercentage === 100) return "Perfect score!";
    if (scorePercentage >= 80) return "Excellent!";
    if (scorePercentage >= 70) return "Great job!";
    if (scorePercentage >= 60) return "Good effort!";
    if (scorePercentage >= 40) return "Keep practicing!";
    return "More study needed!";
  };

  return (
    <div className="quiz-results">
      <h2>Quiz Results</h2>
      
      <div className="score-summary">
        <p className="score-text">You scored: <span className="score-highlight">{correctAnswers}/{totalQuestions}</span></p>
        <p className="percentage">({scorePercentage}%)</p>
        <p className="performance">{getPerformanceText()}</p>
      </div>
      
      <div className="results-breakdown">
        <h3>Question Breakdown:</h3>
        <ul>
          {results.map((answer, index) => (
            <li key={index} className={answer.correct ? "correct" : "incorrect"}>
              Question {answer.id}: {answer.correct ? "✅ Correct" : "❌ Incorrect"}
            </li>
          ))}
        </ul>
      </div>
      
      <button className="restart-button" onClick={() => window.location.reload()}>
        Take Another Quiz
      </button>
    </div>
  );
}
