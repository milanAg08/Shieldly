import React, { useState } from "react";

export default function AvatarBuilder() {
  const [style, setStyle] = useState("Casual");
  const [hair, setHair] = useState("Short");
  const [skinTone, setSkinTone] = useState("Medium");

  return (
    <div className="avatar-builder">
      <h3>🎨 Build Your Avatar</h3>
      <div className="avatar-options">
        <label>
          Hair:
          <select value={hair} onChange={(e) => setHair(e.target.value)}>
            <option>Short</option>
            <option>Long</option>
            <option>Curly</option>
          </select>
        </label>
        <label>
          Style:
          <select value={style} onChange={(e) => setStyle(e.target.value)}>
            <option>Casual</option>
            <option>Sporty</option>
            <option>Fancy</option>
          </select>
        </label>
        <label>
          Skin Tone:
          <select value={skinTone} onChange={(e) => setSkinTone(e.target.value)}>
            <option>Light</option>
            <option>Medium</option>
            <option>Dark</option>
          </select>
        </label>
      </div>
      <div className="avatar-preview">
        <p>👧 Avatar Preview</p>
        <p>
          Hair: {hair}, Style: {style}, Skin Tone: {skinTone}
        </p>
      </div>
    </div>
  );
}
