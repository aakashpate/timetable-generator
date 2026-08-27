import { useState, useEffect } from 'react';
import api from '../api';

export default function ClassesPage() {
  const [classes, setClasses] = useState([]);
  const [form, setForm] = useState({ name: '', year: 1, section: 'A', strength: 60 });

  useEffect(() => { loadClasses(); }, []);

  const loadClasses = async () => {
    const res = await api.getClasses();
    setClasses(res.data);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    await api.createClass({
      ...form,
      year: parseInt(form.year),
      strength: parseInt(form.strength),
    });
    setForm({ name: '', year: 1, section: 'A', strength: 60 });
    loadClasses();
  };

  const handleDelete = async (id) => {
    await api.deleteClass(id);
    loadClasses();
  };

  return (
    <div>
      <div className="card">
        <h2>Add Class/Division</h2>
        <form onSubmit={handleSubmit}>
          <div className="grid-2">
            <div className="form-group">
              <label>Class Name</label>
              <input
                type="text"
                value={form.name}
                onChange={(e) => setForm({ ...form, name: e.target.value })}
                required
                placeholder="e.g. Class 10-A"
              />
            </div>
            <div className="form-group">
              <label>Year</label>
              <input
                type="number"
                min="1"
                max="12"
                value={form.year}
                onChange={(e) => setForm({ ...form, year: e.target.value })}
              />
            </div>
            <div className="form-group">
              <label>Section</label>
              <select
                value={form.section}
                onChange={(e) => setForm({ ...form, section: e.target.value })}
              >
                <option>A</option>
                <option>B</option>
                <option>C</option>
                <option>D</option>
              </select>
            </div>
            <div className="form-group">
              <label>Strength</label>
              <input
                type="number"
                min="1"
                value={form.strength}
                onChange={(e) => setForm({ ...form, strength: e.target.value })}
              />
            </div>
          </div>
          <button type="submit" className="btn btn-primary">Add Class</button>
        </form>
      </div>

      <div className="card">
        <h2>Classes ({classes.length})</h2>
        {classes.length === 0 ? (
          <div className="empty-state"><p>No classes added yet.</p></div>
        ) : (
          <table className="data-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Year</th>
                <th>Section</th>
                <th>Strength</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {classes.map((c) => (
                <tr key={c.id}>
                  <td><strong>{c.name}</strong></td>
                  <td>{c.year}</td>
                  <td>{c.section}</td>
                  <td>{c.strength}</td>
                  <td>
                    <button className="btn btn-danger" onClick={() => handleDelete(c.id)}>Delete</button>
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
