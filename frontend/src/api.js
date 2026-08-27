import axios from 'axios';

const API_BASE = '/api';

const api = {
  // Teachers
  getTeachers: () => axios.get(`${API_BASE}/teachers`),
  createTeacher: (data) => axios.post(`${API_BASE}/teachers`, data),
  deleteTeacher: (id) => axios.delete(`${API_BASE}/teachers/${id}`),

  // Subjects
  getSubjects: () => axios.get(`${API_BASE}/subjects`),
  createSubject: (data) => axios.post(`${API_BASE}/subjects`, data),
  deleteSubject: (id) => axios.delete(`${API_BASE}/subjects/${id}`),

  // Rooms
  getRooms: () => axios.get(`${API_BASE}/rooms`),
  createRoom: (data) => axios.post(`${API_BASE}/rooms`, data),
  deleteRoom: (id) => axios.delete(`${API_BASE}/rooms/${id}`),

  // Classes
  getClasses: () => axios.get(`${API_BASE}/classes`),
  createClass: (data) => axios.post(`${API_BASE}/classes`, data),
  deleteClass: (id) => axios.delete(`${API_BASE}/classes/${id}`),

  // TimeSlots
  getTimeSlots: () => axios.get(`${API_BASE}/timeslots`),
  createTimeSlot: (data) => axios.post(`${API_BASE}/timeslots`, data),

  // Availability
  getAvailability: (teacherId) => axios.get(`${API_BASE}/availability/${teacherId}`),
  setAvailability: (data) => axios.post(`${API_BASE}/availability`, data),

  // Timetable
  generateTimetable: (name) => axios.post(`${API_BASE}/timetable/generate`, { name }),
  getTimetable: (id) => axios.get(`${API_BASE}/timetable/${id}`),
  getTimetables: () => axios.get(`${API_BASE}/timetables`),
  deleteTimetable: (id) => axios.delete(`${API_BASE}/timetable/${id}`),
};

export default api;
