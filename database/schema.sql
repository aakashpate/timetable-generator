-- Timetable Generator Database Schema

CREATE TABLE IF NOT EXISTS teachers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    employee_id VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(100),
    department VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS subjects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20) UNIQUE NOT NULL,
    subject_type VARCHAR(20) DEFAULT 'theory',
    lectures_per_week INTEGER NOT NULL,
    requires_lab BOOLEAN DEFAULT FALSE,
    teacher_id INTEGER REFERENCES teachers(id)
);

CREATE TABLE IF NOT EXISTS rooms (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    room_number VARCHAR(20) UNIQUE NOT NULL,
    capacity INTEGER NOT NULL,
    is_lab BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS time_slots (
    id SERIAL PRIMARY KEY,
    period_number INTEGER NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL
);

CREATE TABLE IF NOT EXISTS class_divisions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    year INTEGER NOT NULL,
    section VARCHAR(10) NOT NULL,
    strength INTEGER DEFAULT 60
);

CREATE TABLE IF NOT EXISTS teacher_availability (
    id SERIAL PRIMARY KEY,
    teacher_id INTEGER REFERENCES teachers(id),
    day VARCHAR(20) NOT NULL,
    period_number INTEGER NOT NULL,
    is_available BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS timetables (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    fitness_score INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at VARCHAR(30)
);

CREATE TABLE IF NOT EXISTS lectures (
    id SERIAL PRIMARY KEY,
    timetable_id INTEGER REFERENCES timetables(id) ON DELETE CASCADE,
    class_division_id INTEGER REFERENCES class_divisions(id),
    subject_id INTEGER REFERENCES subjects(id),
    teacher_id INTEGER REFERENCES teachers(id),
    room_id INTEGER REFERENCES rooms(id),
    time_slot_id INTEGER REFERENCES time_slots(id),
    day VARCHAR(20) NOT NULL
);
