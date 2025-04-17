import React from "react";

const moods = ["😊 Happy", "😢 Sad", "😠 Angry", "😨 Scared", "😐 Okay"];

export default function MoodSelector({ mood, setMood }) {
  return (
    <div className="mood-selector">
      <h3>How are you feeling today?</h3>
      <div className="mood-options">
        {moods.map((m) => (
          <button
            key={m}
            className={`mood-btn ${m === mood ? "selected" : ""}`}
            onClick={() => setMood(m)}
          >
            {m}
          </button>
        ))}
      </div>
    </div>
  );
}
