import { useState, useEffect } from 'react';
import api from '../api';

export default function SubjectsPage() {
  const [subjects, setSubjects] = useState([]);
  const [teachers, setTeachers] = useState([]);
  const [form, setForm] = useState({
    name: '', code: '', subject_type: 'theory',
    lectures_per_week: 3, requires_lab: false, teacher_id: ''
  });

  useEffect(() => {
    loadSubjects();
    loadTeachers();
  }, []);

  const loadSubjects = async () => {
    const res = await api.getSubjects();
    setSubjects(res.data);
  };

  const loadTeachers = async () => {
    const res = await api.getTeachers();
    setTeachers(res.data);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    await api.createSubject({
      ...form,
      teacher_id: parseInt(form.teacher_id),
      lectures_per_week: parseInt(form.lectures_per_week),
    });
    setForm({ name: '', code: '', subject_type: 'theory', lectures_per_week: 3, requires_lab: false, teacher_id: '' });
    loadSubjects();
  };

  const handleDelete = async (id) => {
    await api.deleteSubject(id);
    loadSubjects();
  };

  const getTeacherName = (id) => {
    const t = teachers.find((t) => t.id === id);
    return t ? t.name : 'Unassigned';
  };

  return (
    <div>
      <div className="card">
        <h2>Add Subject</h2>
        <form onSubmit={handleSubmit}>
          <div className="grid-2">
            <div className="form-group">
              <label>Subject Name</label>
              <input
                type="text"
                value={form.name}
                onChange={(e) => setForm({ ...form, name: e.target.value })}
                required
                placeholder="e.g. Mathematics"
              />
            </div>
            <div className="form-group">
              <label>Subject Code</label>
              <input
                type="text"
                value={form.code}
                onChange={(e) => setForm({ ...form, code: e.target.value })}
                required
                placeholder="e.g. MATH101"
              />
            </div>
            <div className="form-group">
              <label>Type</label>
              <select
                value={form.subject_type}
                onChange={(e) => setForm({ ...form, subject_type: e.target.value })}
              >
                <option value="theory">Theory</option>
                <option value="practical">Practical</option>
                <option value="lab">Lab</option>
              </select>
            </div>
            <div className="form-group">
              <label>Lectures per Week</label>
              <input
                type="number"
                min="1"
                max="10"
                value={form.lectures_per_week}
                onChange={(e) => setForm({ ...form, lectures_per_week: e.target.value })}
              />
            </div>
            <div className="form-group">
              <label>Assigned Teacher</label>
              <select
                value={form.teacher_id}
                onChange={(e) => setForm({ ...form, teacher_id: e.target.value })}
                required
              >
                <option value="">Select Teacher</option>
                {teachers.map((t) => (
                  <option key={t.id} value={t.id}>{t.name} ({t.employee_id})</option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginTop: '1.5rem' }}>
                <input
                  type="checkbox"
                  checked={form.requires_lab}
                  onChange={(e) => setForm({ ...form, requires_lab: e.target.checked })}
                />
                Requires Lab
              </label>
            </div>
          </div>
          <button type="submit" className="btn btn-primary">Add Subject</button>
        </form>
      </div>

      <div className="card">
        <h2>Subjects ({subjects.length})</h2>
        {subjects.length === 0 ? (
          <div className="empty-state"><p>No subjects added yet.</p></div>
        ) : (
          <table className="data-table">
            <thead>
              <tr>
                <th>Code</th>
                <th>Name</th>
                <th>Type</th>
                <th>Lectures/Week</th>
                <th>Teacher</th>
                <th>Lab Required</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {subjects.map((s) => (
                <tr key={s.id}>
                  <td><strong>{s.code}</strong></td>
                  <td>{s.name}</td>
                  <td>
                    <span style={{
                      padding: '0.2rem 0.5rem',
                      borderRadius: '4px',
                      background: s.subject_type === 'lab' ? '#dcfce7' : s.subject_type === 'practical' ? '#f3e8ff' : '#dbeafe',
                      fontSize: '0.8rem',
                      fontWeight: 600,
                    }}>
                      {s.subject_type}
                    </span>
                  </td>
                  <td>{s.lectures_per_week}</td>
                  <td>{getTeacherName(s.teacher_id)}</td>
                  <td>{s.requires_lab ? 'Yes' : 'No'}</td>
                  <td>
                    <button className="btn btn-danger" onClick={() => handleDelete(s.id)}>Delete</button>
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
