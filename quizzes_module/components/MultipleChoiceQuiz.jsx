
import quizzes_en from "../data/quizzes_en.json";
import quizzes_hi from "../data/quizzes_hi.json";
import CategoryFilter from "./CategoryFilter";
import "../styles/quizStyles.css";
import React, { useState, useEffect, useRef } from "react";
const [theme, setTheme] = useState("light");


// 🔁 Shuffle utility
function shuffleArray(array) {
  const shuffled = [...array];
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
  }
  return shuffled;
}

// 🌐 Load quiz data by language
const getQuizData = (language) => {
  switch (language) {
    case "hi":
      return quizzes_hi;
    case "en":
    default:
      return quizzes_en;
  }
};

// 🌟 Reward stars
const getStarsForScore = (score, total) => {
  const ratio = score / total;
  if (ratio === 1) return "🌟🌟🌟 Perfect!";
  if (ratio >= 0.7) return "🌟🌟 Great job!";
  if (ratio >= 0.4) return "🌟 Good effort!";
  return "💡 Keep practicing!";
};

export default function MultipleChoiceQuiz({ language = "en", onSubmit }) {
  const audioRef = useRef(null);

  const rawData = getQuizData(language);

  const [selectedCategory, setSelectedCategory] = useState("");
  const [quizData, setQuizData] = useState([]);
  const [current, setCurrent] = useState(0);
  const [selected, setSelected] = useState(null);
  const [answers, setAnswers] = useState([]);
  const [showHint, setShowHint] = useState(false);
  const [feedback, setFeedback] = useState("");
  const [explanation, setExplanation] = useState("");
  const [showResults, setShowResults] = useState(false);
  const [timeLeft, setTimeLeft] = useState(15);
  useEffect(() => {
    if (audioRef.current) {
      audioRef.current.pause(); // Stop previous audio
      audioRef.current.currentTime = 0;
    }
  
    const currentAudio = question.audio;
    if (currentAudio) {
      const audio = new Audio(currentAudio);
      audioRef.current = audio;
      audio.play();
    }
  }, [current]); // Trigger when question changes
  

  // ⬇️ Unique categories
  const categories = [...new Set(rawData.map((q) => q.category))];

  // ⏱️ Timer countdown
  useEffect(() => {
    if (showResults) return;

    if (timeLeft === 0) {
      handleNext(); // Auto move
      return;
    }

    const timer = setTimeout(() => {
      setTimeLeft(timeLeft - 1);
    }, 1000);

    return () => clearTimeout(timer);
  }, [timeLeft, showResults]);

  // 🔁 Filtered quiz data on category change
  useEffect(() => {
    const filtered = selectedCategory
      ? rawData.filter((q) => q.category === selectedCategory)
      : rawData;

    setQuizData(shuffleArray(filtered));
    setCurrent(0);
    setAnswers([]);
    setSelected(null);
    setShowHint(false);
    setFeedback("");
    setShowResults(false);
    setTimeLeft(15);
  }, [selectedCategory]);

  const handleOptionClick = (index) => {
    setSelected(index);
  };

  const handleNext = () => {
    const isCorrect = selected === quizData[current].correctIndex;
    const updatedAnswers = [...answers, { id: current + 1, correct: isCorrect }];
    setAnswers(updatedAnswers);
    setFeedback(isCorrect ? "✅ Correct!" : "❌ Oops! That's not right.");
    setExplanation(quizData[current].explanation);

    setShowHint(false);
    setSelected(null);

    if (current + 1 < quizData.length) {
      setTimeLeft(15); // Reset timer
      setCurrent(current + 1);
      setTimeout(() => setFeedback(""), 1000);
      setExplanation("");
    } else {
      setShowResults(true);
      if (onSubmit) onSubmit(updatedAnswers);
    }
  };

  const handleRestart = () => {
    setSelectedCategory("");
  };

  const question = quizData[current];

  return (
    <div className={`quiz-container ${theme}`}>

      <CategoryFilter
        categories={categories}
        selectedCategory={selectedCategory}
        onChange={setSelectedCategory}
      />

      {showResults ? (
        <div>
          <h2 className="quiz-header">🎉 Quiz Complete!</h2>
          <p>
            You got {answers.filter((a) => a.correct).length} out of {quizData.length} correct.
          </p>
          <p style={{ fontSize: "24px", marginTop: "10px" }}>
            {getStarsForScore(answers.filter((a) => a.correct).length, quizData.length)}
          </p>
          <button onClick={handleRestart}>🔁 Restart Quiz</button>
        </div>
      ) : question ? (
        <>
          {/* 🔄 Progress Bar */}
          <div
            style={{
              height: "10px",
              background: "#ccc",
              borderRadius: "5px",
              marginBottom: "20px",
            }}
          >
            <div
              style={{
                height: "100%",
                width: `${((current + 1) / quizData.length) * 100}%`,
                backgroundColor: "#4caf50",
                borderRadius: "5px",
                transition: "width 0.4s ease-in-out",
              }}
            />
          </div>

          {/* ⏱️ Timer */}
          <p style={{ fontWeight: "bold", color: timeLeft <= 5 ? "red" : "#333" }}>
            ⏳ Time left: {timeLeft} seconds
          </p>

          {/* ❓ Question */}
          <h3 className="quiz-header">Q{current + 1}: {question.question}</h3>
          {question.audio && (
            <audio ref={audioRef} controls style={{ marginBottom: "10px" }}>
              <source src={`/${question.audio}`} type="audio/mpeg" />
               Your browser does not support the audio element.
            </audio>
          )}


          <button
            onClick={() => setShowHint(true)}
            style={{
              marginBottom: "10px",
              padding: "6px 10px",
              borderRadius: "6px",
              backgroundColor: "#ffd54f",
              border: "none",
              cursor: "pointer",
            }}
          >
            Show Hint
          </button>

          {showHint && (
            <p style={{ fontStyle: "italic", color: "#666" }}>{question.hint}</p>
          )}

          {feedback && (
            <p style={{ fontWeight: "bold", color: feedback.startsWith("✅") ? "green" : "red" }}>
              {feedback}
            </p>
          )}

          {explanation && (
            <p style={{ marginTop: "10px", fontStyle: "italic", color: "#444" }}>
              💡 {explanation}
            </p>
          )}

          {/* 🔘 Options */}
          <ul style={{ listStyle: "none", padding: 0 }}>
            {question.options.map((option, index) => (
              <li key={index}>
                <button
                  onClick={() => handleOptionClick(index)}
                  className={`quiz-button ${selected === index ? "selected" : ""}`}
                >
                  {option}
                </button>
              </li>
            ))}
          </ul>

          <button onClick={handleNext} disabled={selected === null}>
            {current + 1 === quizData.length ? "Finish Quiz" : "Next"}
          </button>
        </>
      ) : (
        <p>No questions available for this category.</p>
      )}
    </div>
  );
}
