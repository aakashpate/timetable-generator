import { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import TeachersPage from './pages/TeachersPage';
import SubjectsPage from './pages/SubjectsPage';
import RoomsPage from './pages/RoomsPage';
import ClassesPage from './pages/ClassesPage';
import GeneratePage from './pages/GeneratePage';
import ViewTimetablePage from './pages/ViewTimetablePage';
import './App.css';

function App() {
  return (
    <Router>
      <div className="app">
        <header>
          <h1>Timetable Generator</h1>
          <nav>
            <Link to="/teachers">Teachers</Link>
            <Link to="/subjects">Subjects</Link>
            <Link to="/rooms">Rooms</Link>
            <Link to="/classes">Classes</Link>
            <Link to="/generate">Generate</Link>
          </nav>
        </header>

        <div className="container">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/teachers" element={<TeachersPage />} />
            <Route path="/subjects" element={<SubjectsPage />} />
            <Route path="/rooms" element={<RoomsPage />} />
            <Route path="/classes" element={<ClassesPage />} />
            <Route path="/generate" element={<GeneratePage />} />
            <Route path="/timetable/:id" element={<ViewTimetablePage />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

function HomePage() {
  return (
    <div className="card">
      <h2>Welcome to Timetable Generator</h2>
      <p style={{ color: 'var(--text-muted)', marginBottom: '1.5rem' }}>
        Automatically generate conflict-free timetables using constraint-based optimization.
      </p>
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-label">Step 1</div>
          <div className="stat-value" style={{ fontSize: '1rem' }}>Add Teachers</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Step 2</div>
          <div className="stat-value" style={{ fontSize: '1rem' }}>Add Subjects</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Step 3</div>
          <div className="stat-value" style={{ fontSize: '1rem' }}>Add Rooms & Classes</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Step 4</div>
          <div className="stat-value" style={{ fontSize: '1rem' }}>Generate Timetable</div>
        </div>
      </div>
      <Link to="/generate" className="btn btn-primary">Get Started</Link>
    </div>
  );
}

export default App;
