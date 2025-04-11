import React, { useState } from "react";
import MultipleChoiceQuiz from "./MultipleChoiceQuiz";
import QuizResultsTest from "./QuizResultsTest";

export default function QuizApp() {
  const [results, setResults] = useState(null);

  return (
    <div>
      {!results ? (
        <MultipleChoiceQuiz onSubmit={(data) => setResults(data)} />
      ) : (
        <QuizResultsTest results={results} />
      )}
    </div>
  );
}
