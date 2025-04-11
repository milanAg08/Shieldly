import React from "react";

export default function LanguageToggle({ language, onChange }) {
  return (
    <div style={{ marginBottom: "20px", textAlign: "center" }}>
      <label style={{ marginRight: "10px", fontWeight: "bold" }}>Language:</label>
      <select value={language} onChange={(e) => onChange(e.target.value)}>
        <option value="en">English</option>
        <option value="hi">हिन्दी</option>
      </select>
    </div>
  );
}
