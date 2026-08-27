-- Seed data for Timetable Generator

-- Time Slots (8 periods)
INSERT INTO time_slots (period_number, start_time, end_time) VALUES
(1, '08:00', '08:50'),
(2, '09:00', '09:50'),
(3, '10:00', '10:50'),
(4, '11:00', '11:50'),
(5, '12:00', '12:50'),
(6, '14:00', '14:50'),
(7, '15:00', '15:50'),
(8, '16:00', '16:50');

-- Teachers
INSERT INTO teachers (name, employee_id, email, department) VALUES
('Dr. Ramesh Kumar', 'T001', 'ramesh@school.edu', 'Mathematics'),
('Prof. Sunita Sharma', 'T002', 'sunita@school.edu', 'Physics'),
('Mr. Amit Patel', 'T003', 'amit@school.edu', 'Chemistry'),
('Mrs. Priya Desai', 'T004', 'priya@school.edu', 'English'),
('Dr. Vikram Singh', 'T005', 'vikram@school.edu', 'Computer Science'),
('Ms. Neha Gupta', 'T006', 'neha@school.edu', 'Biology');

-- Subjects
INSERT INTO subjects (name, code, subject_type, lectures_per_week, requires_lab, teacher_id) VALUES
('Mathematics', 'MATH101', 'theory', 5, FALSE, 1),
('Physics', 'PHY101', 'theory', 4, FALSE, 2),
('Physics Lab', 'PHY101L', 'lab', 1, TRUE, 2),
('Chemistry', 'CHM101', 'theory', 4, FALSE, 3),
('Chemistry Lab', 'CHM101L', 'lab', 1, TRUE, 3),
('English', 'ENG101', 'theory', 4, FALSE, 4),
('Computer Science', 'CS101', 'theory', 3, FALSE, 5),
('CS Lab', 'CS101L', 'lab', 2, TRUE, 5),
('Biology', 'BIO101', 'theory', 3, FALSE, 6);

-- Rooms
INSERT INTO rooms (name, room_number, capacity, is_lab) VALUES
('Room 101', 'R101', 60, FALSE),
('Room 102', 'R102', 60, FALSE),
('Room 103', 'R103', 40, FALSE),
('Physics Lab', 'PL01', 30, TRUE),
('Chemistry Lab', 'CL01', 30, TRUE),
('CS Lab', 'CSL01', 30, TRUE),
('Room 201', 'R201', 60, FALSE),
('Room 202', 'R202', 40, FALSE);

-- Classes
INSERT INTO class_divisions (name, year, section, strength) VALUES
('Class 10-A', 10, 'A', 45),
('Class 10-B', 10, 'B', 42),
('Class 11-A', 11, 'A', 40);
