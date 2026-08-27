import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import api from '../api';

const DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
const PERIODS = [1, 2, 3, 4, 5, 6, 7, 8];

export default function ViewTimetablePage() {
  const { id } = useParams();
  const [timetable, setTimetable] = useState(null);
  const [grid, setGrid] = useState({});
  const [selectedClass, setSelectedClass] = useState(null);
  const [classes, setClasses] = useState([]);
  const [view, setView] = useState('class');

  useEffect(() => {
    loadTimetable();
  }, [id]);

  const loadTimetable = async () => {
    try {
      const res = await api.getTimetable(id);
      setTimetable(res.data);

      const classMap = {};
      const classSet = new Set();
      res.data.lectures.forEach((lec) => {
        classSet.add(lec.class_division_id);
        const key = `${lec.class_division_id}-${lec.day}-${lec.period_number}`;
        classMap[key] = lec;
      });

      setGrid(classMap);
      const classList = Array.from(classSet).map((cid) => ({
        id: cid,
        name: res.data.lectures.find((l) => l.class_division_id === cid)?.class_division_id || `Class ${cid}`,
      }));

      const classRes = await api.getClasses();
      const fullClasses = classRes.data.filter((c) => classSet.has(c.id));
      setClasses(fullClasses);

      if (fullClasses.length > 0) {
        setSelectedClass(fullClasses[0].id);
      }
    } catch (err) {
      console.error('Failed to load timetable', err);
    }
  };

  const getCell = (classId, day, period) => {
    const key = `${classId}-${day}-${period}`;
    return grid[key] || null;
  };

  const handlePrint = () => {
    window.print();
  };

  if (!timetable) return <div className="empty-state"><p>Loading timetable...</p></div>;

  return (
    <div>
      <div className="card" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h2>{timetable.name}</h2>
          <span className={`fitness-badge ${
            timetable.fitness_score >= 80 ? 'fitness-high' :
            timetable.fitness_score >= 50 ? 'fitness-medium' : 'fitness-low'
          }`}>
            Fitness: {timetable.fitness_score}%
          </span>
        </div>
        <div className="btn-group">
          <button className="btn btn-primary" onClick={handlePrint}>Print</button>
        </div>
      </div>

      {classes.length > 0 && (
        <div className="card">
          <div className="legend">
            <div className="legend-item">
              <div className="legend-dot" style={{ background: 'var(--theory)' }}></div>
              Theory
            </div>
            <div className="legend-item">
              <div className="legend-dot" style={{ background: 'var(--practical)' }}></div>
              Practical
            </div>
            <div className="legend-item">
              <div className="legend-dot" style={{ background: 'var(--lab)' }}></div>
              Lab
            </div>
          </div>

          <div style={{ marginBottom: '1rem' }}>
            <label style={{ fontWeight: 600, marginRight: '0.5rem' }}>Select Class:</label>
            <select
              value={selectedClass || ''}
              onChange={(e) => setSelectedClass(parseInt(e.target.value))}
              style={{ padding: '0.5rem', borderRadius: '6px', border: '1px solid var(--border)' }}
            >
              {classes.map((c) => (
                <option key={c.id} value={c.id}>{c.name}</option>
              ))}
            </select>
          </div>

          {selectedClass && (
            <div style={{ overflowX: 'auto' }}>
              <table className="timetable-grid">
                <thead>
                  <tr>
                    <th>Day / Period</th>
                    {PERIODS.map((p) => (
                      <th key={p}>Period {p}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {DAYS.map((day) => (
                    <tr key={day}>
                      <td style={{ fontWeight: 700, background: '#f1f5f9' }}>{day}</td>
                      {PERIODS.map((period) => {
                        const cell = getCell(selectedClass, day, period);
                        if (cell) {
                          return (
                            <td key={period} className={`cell-${cell.subject_type || 'theory'}`}>
                              <div className="cell-subject">{cell.subject_name}</div>
                              <div className="cell-teacher">{cell.teacher_name}</div>
                              <div className="cell-room">{cell.room_name}</div>
                            </td>
                          );
                        }
                        return (
                          <td key={period} className="empty-cell">-</td>
                        );
                      })}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}

      {classes.length === 0 && (
        <div className="card empty-state">
          <p>No lectures found in this timetable.</p>
        </div>
      )}
    </div>
  );
}
