import { useState, useEffect } from "react";

export default function useJournalStorage() {
  const [entries, setEntries] = useState([]);

  useEffect(() => {
    const saved = localStorage.getItem("journalEntries");
    if (saved) {
      setEntries(JSON.parse(saved));
    }
  }, []);

  const saveEntry = (entry) => {
    const updated = [...entries, entry];
    setEntries(updated);
    localStorage.setItem("journalEntries", JSON.stringify(updated));
  };

  return { entries, saveEntry };
}
