import { useState, useEffect } from 'react';
import api from '../api';

export default function TeachersPage() {
  const [teachers, setTeachers] = useState([]);
  const [form, setForm] = useState({ name: '', employee_id: '', email: '', department: '' });

  useEffect(() => { loadTeachers(); }, []);

  const loadTeachers = async () => {
    const res = await api.getTeachers();
    setTeachers(res.data);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    await api.createTeacher(form);
    setForm({ name: '', employee_id: '', email: '', department: '' });
    loadTeachers();
  };

  const handleDelete = async (id) => {
    await api.deleteTeacher(id);
    loadTeachers();
  };

  return (
    <div>
      <div className="card">
        <h2>Add Teacher</h2>
        <form onSubmit={handleSubmit}>
          <div className="grid-2">
            <div className="form-group">
              <label>Full Name</label>
              <input
                type="text"
                value={form.name}
                onChange={(e) => setForm({ ...form, name: e.target.value })}
                required
                placeholder="e.g. Dr. Smith"
              />
            </div>
            <div className="form-group">
              <label>Employee ID</label>
              <input
                type="text"
                value={form.employee_id}
                onChange={(e) => setForm({ ...form, employee_id: e.target.value })}
                required
                placeholder="e.g. T001"
              />
            </div>
            <div className="form-group">
              <label>Email</label>
              <input
                type="email"
                value={form.email}
                onChange={(e) => setForm({ ...form, email: e.target.value })}
                placeholder="teacher@school.edu"
              />
            </div>
            <div className="form-group">
              <label>Department</label>
              <input
                type="text"
                value={form.department}
                onChange={(e) => setForm({ ...form, department: e.target.value })}
                placeholder="e.g. Mathematics"
              />
            </div>
          </div>
          <button type="submit" className="btn btn-primary">Add Teacher</button>
        </form>
      </div>

      <div className="card">
        <h2>Teachers ({teachers.length})</h2>
        {teachers.length === 0 ? (
          <div className="empty-state">
            <p>No teachers added yet.</p>
          </div>
        ) : (
          <table className="data-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Employee ID</th>
                <th>Email</th>
                <th>Department</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {teachers.map((t) => (
                <tr key={t.id}>
                  <td><strong>{t.name}</strong></td>
                  <td>{t.employee_id}</td>
                  <td>{t.email || '-'}</td>
                  <td>{t.department || '-'}</td>
                  <td>
                    <button className="btn btn-danger" onClick={() => handleDelete(t.id)}>
                      Delete
                    </button>
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
