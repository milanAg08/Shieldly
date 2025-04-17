import React from "react";
import { BrowserRouter as Router, Routes, Route, NavLink } from "react-router-dom";
import Header from "./components/Layout/Header";
import Footer from "./components/Layout/Footer";
import Journal from "./pages/Journal";
import Stories from "./pages/Stories";
import Avatar from "./pages/Avatar";
import "./styles/emotional.css";

export default function App() {
  return (
    <Router>
      <div className="app-container">
        <Header />
        <main className="main-content">
          <nav className="main-nav">
            <NavLink to="/journal">📝 Journal</NavLink>
            <NavLink to="/stories">📖 Stories</NavLink>
            <NavLink to="/avatar">🎨 Avatar</NavLink>
          </nav>
          <Routes>
            <Route path="/journal" element={<Journal />} />
            <Route path="/stories" element={<Stories />} />
            <Route path="/avatar" element={<Avatar />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}
