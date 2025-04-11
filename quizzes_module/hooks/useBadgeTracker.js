import { useState, useEffect } from "react";

// Custom hook to track which badges are unlocked
export default function useBadgeTracker(quizResults) {
  const [badges, setBadges] = useState([]);

  useEffect(() => {
    if (!quizResults || quizResults.length === 0) return;

    const score = quizResults.filter(q => q.correct).length;
    let unlocked = [];

    if (score >= 1 && !badges.includes("Beginner")) {
      unlocked.push("Beginner");
    }

    if (score >= 2 && !badges.includes("Confident Protector")) {
      unlocked.push("Confident Protector");
    }

    if (unlocked.length > 0) {
      setBadges(prev => [...new Set([...prev, ...unlocked])]);
    }
  }, [quizResults]);

  return badges;
}
