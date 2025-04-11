import React, { useState } from "react";
import MoodSelector from "../components/MoodSelector";
import JournalEntryForm from "../components/JournalEntryForm";
import useJournalStorage from "../hooks/useJournalStorage";

export default function Journal() {
  const [mood, setMood] = useState("");
  const { entries, addEntry } = useJournalStorage();

  return (
    <div className="journal-page">
      <MoodSelector mood={mood} setMood={setMood} />
      <JournalEntryForm onSubmit={addEntry} />
      <div className="entries-list">
        <h3>Your Entries</h3>
        {entries.map((e) => (
          <div key={e.id} className="entry-card">
            <p><strong>{e.date}</strong></p>
            <p>{e.text}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
