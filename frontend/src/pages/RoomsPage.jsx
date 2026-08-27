import { useState, useEffect } from 'react';
import api from '../api';

export default function RoomsPage() {
  const [rooms, setRooms] = useState([]);
  const [form, setForm] = useState({ name: '', room_number: '', capacity: 60, is_lab: false });

  useEffect(() => { loadRooms(); }, []);

  const loadRooms = async () => {
    const res = await api.getRooms();
    setRooms(res.data);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    await api.createRoom({ ...form, capacity: parseInt(form.capacity) });
    setForm({ name: '', room_number: '', capacity: 60, is_lab: false });
    loadRooms();
  };

  const handleDelete = async (id) => {
    await api.deleteRoom(id);
    loadRooms();
  };

  return (
    <div>
      <div className="card">
        <h2>Add Room</h2>
        <form onSubmit={handleSubmit}>
          <div className="grid-2">
            <div className="form-group">
              <label>Room Name</label>
              <input
                type="text"
                value={form.name}
                onChange={(e) => setForm({ ...form, name: e.target.value })}
                required
                placeholder="e.g. Room 101"
              />
            </div>
            <div className="form-group">
              <label>Room Number</label>
              <input
                type="text"
                value={form.room_number}
                onChange={(e) => setForm({ ...form, room_number: e.target.value })}
                required
                placeholder="e.g. R101"
              />
            </div>
            <div className="form-group">
              <label>Capacity</label>
              <input
                type="number"
                min="1"
                value={form.capacity}
                onChange={(e) => setForm({ ...form, capacity: e.target.value })}
              />
            </div>
            <div className="form-group">
              <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginTop: '1.5rem' }}>
                <input
                  type="checkbox"
                  checked={form.is_lab}
                  onChange={(e) => setForm({ ...form, is_lab: e.target.checked })}
                />
                Is Lab
              </label>
            </div>
          </div>
          <button type="submit" className="btn btn-primary">Add Room</button>
        </form>
      </div>

      <div className="card">
        <h2>Rooms ({rooms.length})</h2>
        {rooms.length === 0 ? (
          <div className="empty-state"><p>No rooms added yet.</p></div>
        ) : (
          <table className="data-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Number</th>
                <th>Capacity</th>
                <th>Type</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {rooms.map((r) => (
                <tr key={r.id}>
                  <td><strong>{r.name}</strong></td>
                  <td>{r.room_number}</td>
                  <td>{r.capacity}</td>
                  <td>{r.is_lab ? 'Lab' : 'Classroom'}</td>
                  <td>
                    <button className="btn btn-danger" onClick={() => handleDelete(r.id)}>Delete</button>
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
