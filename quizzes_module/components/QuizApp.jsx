import React, { useState } from "react";
import MultipleChoiceQuiz from "./MultipleChoiceQuiz";
import QuizResultsTest from "./QuizResultsTest";
import LanguageToggle from "./LanguageToggle";

export default function QuizApp() {
  const [results, setResults] = useState(null);
  const [language, setLanguage] = useState("en");

  const handleReset = () => {
    setResults(null);
  };

  return (
    <div>
      <LanguageToggle language={language} onChange={setLanguage} />
      
      {!results ? (
        <MultipleChoiceQuiz 
          language={language} 
          onSubmit={(data) => setResults(data)} 
        />
      ) : (
        <QuizResultsTest 
          results={results} 
          onReset={handleReset}
        />
      )}
    </div>
  );
}
