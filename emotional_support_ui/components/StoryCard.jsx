import React from "react";

export default function StoryCard({ story }) {
  return (
    <div className="story-card">
      <p>"{story.text}"</p>
      {story.audio && (
        <audio controls>
          <source src={`/${story.audio}`} type="audio/mpeg" />
          Your browser does not support the audio element.
        </audio>
      )}
    </div>
  );
}
