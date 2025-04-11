import React, { useState } from "react";
import MultipleChoiceQuiz from "./MultipleChoiceQuiz";
import LanguageToggle from "./LanguageToggle";

export default function QuizResultsTest() {
  const [language, setLanguage] = useState("en");

  const handleResults = (results) => {
    console.log("Quiz completed. Results:", results);
  };

  return (
    <div>
      <LanguageToggle language={language} onChange={setLanguage} />
      <MultipleChoiceQuiz language={language} onSubmit={handleResults} />
    </div>
  );
}

