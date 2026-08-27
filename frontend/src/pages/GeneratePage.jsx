import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';

export default function GeneratePage() {
  const navigate = useNavigate();
  const [name, setName] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [timetables, setTimetables] = useState([]);
  const [teachers, setTeachers] = useState([]);
  const [subjects, setSubjects] = useState([]);
  const [rooms, setRooms] = useState([]);
  const [classes, setClasses] = useState([]);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    const [t, s, r, c, tt] = await Promise.all([
      api.getTeachers(),
      api.getSubjects(),
      api.getRooms(),
      api.getClasses(),
      api.getTimetables(),
    ]);
    setTeachers(t.data);
    setSubjects(s.data);
    setRooms(r.data);
    setClasses(c.data);
    setTimetables(tt.data);
  };

  const handleGenerate = async (e) => {
    e.preventDefault();
    if (!name.trim()) return;
    setLoading(true);
    try {
      const res = await api.generateTimetable(name);
      setResult(res.data);
      loadData();
    } catch (err) {
      alert(err.response?.data?.detail || 'Error generating timetable');
    } finally {
      setLoading(false);
    }
  };

  const handleView = (id) => {
    navigate(`/timetable/${id}`);
  };

  const handleDelete = async (id) => {
    await api.deleteTimetable(id);
    loadData();
  };

  const canGenerate = teachers.length > 0 && subjects.length > 0 && rooms.length > 0 && classes.length > 0;

  return (
    <div>
      <div className="card">
        <h2>Generate Timetable</h2>
        {!canGenerate && (
          <div style={{ padding: '1rem', background: '#fef3c7', borderRadius: '8px', marginBottom: '1rem' }}>
            <strong>Prerequisites:</strong> Add at least 1 teacher, 1 subject, 1 room, and 1 class before generating.
            <br />
            Current: {teachers.length} teachers, {subjects.length} subjects, {rooms.length} rooms, {classes.length} classes.
          </div>
        )}
        <form onSubmit={handleGenerate}>
          <div className="grid-2">
            <div className="form-group">
              <label>Timetable Name</label>
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
                placeholder="e.g. Fall 2026 Schedule"
              />
            </div>
          </div>
          <button
            type="submit"
            className="btn btn-success"
            disabled={loading || !canGenerate}
          >
            {loading ? 'Generating...' : 'Generate Timetable'}
          </button>
        </form>
      </div>

      {result && (
        <div className="card">
          <h2>Generation Result</h2>
          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-value">
                <span className={`fitness-badge ${
                  result.timetable.fitness_score >= 80 ? 'fitness-high' :
                  result.timetable.fitness_score >= 50 ? 'fitness-medium' : 'fitness-low'
                }`}>
                  {result.timetable.fitness_score}%
                </span>
              </div>
              <div className="stat-label">Fitness Score</div>
            </div>
            <div className="stat-card">
              <div className="stat-value">{result.lectures.length}</div>
              <div className="stat-label">Lectures Scheduled</div>
            </div>
            <div className="stat-card">
              <div className="stat-value">{result.conflicts.length}</div>
              <div className="stat-label">Conflicts</div>
            </div>
          </div>

          {result.conflicts.length > 0 && (
            <div style={{ marginBottom: '1rem' }}>
              <strong>Conflicts:</strong>
              <ul className="conflict-list">
                {result.conflicts.map((c, i) => (
                  <li key={i}>{c.message}</li>
                ))}
              </ul>
            </div>
          )}

          <div className="btn-group">
            <button className="btn btn-primary" onClick={() => handleView(result.timetable.id)}>
              View Timetable
            </button>
          </div>
        </div>
      )}

      <div className="card">
        <h2>Saved Timetables ({timetables.length})</h2>
        {timetables.length === 0 ? (
          <div className="empty-state"><p>No timetables generated yet.</p></div>
        ) : (
          <table className="data-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Fitness Score</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {timetables.map((tt) => (
                <tr key={tt.id}>
                  <td><strong>{tt.name}</strong></td>
                  <td>
                    <span className={`fitness-badge ${
                      tt.fitness_score >= 80 ? 'fitness-high' :
                      tt.fitness_score >= 50 ? 'fitness-medium' : 'fitness-low'
                    }`}>
                      {tt.fitness_score}%
                    </span>
                  </td>
                  <td>{tt.is_active ? 'Active' : 'Inactive'}</td>
                  <td>
                    <div className="btn-group">
                      <button className="btn btn-primary" onClick={() => handleView(tt.id)}>
                        View
                      </button>
                      <button className="btn btn-danger" onClick={() => handleDelete(tt.id)}>
                        Delete
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
