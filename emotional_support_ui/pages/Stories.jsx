import React from "react";
import StoryCard from "../components/StoryCard";
import stories from "../data/stories_en.json";

export default function Stories() {
  return (
    <div className="stories-page">
      <h2>📚 You’re Not Alone</h2>
      {stories.map((story, index) => (
        <StoryCard key={index} story={story} />
      ))}
    </div>
  );
}
