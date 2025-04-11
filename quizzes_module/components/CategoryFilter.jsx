import React from "react";

export default function CategoryFilter({ categories, selectedCategory, onChange }) {
  return (
    <div style={{ marginBottom: "20px" }}>
      <label htmlFor="categorySelect" style={{ marginRight: "10px", fontWeight: "bold" }}>
        Filter by Category:
      </label>
      <select
        id="categorySelect"
        value={selectedCategory}
        onChange={(e) => onChange(e.target.value)}
        style={{ padding: "5px 10px", borderRadius: "6px" }}
      >
        <option value="">All</option>
        {categories.map((cat, index) => (
          <option key={index} value={cat}>
            {cat}
          </option>
        ))}
      </select>
    </div>
  );
}
