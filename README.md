# Timetable Generator

A full-stack web application that automatically generates conflict-free timetables using **Constraint Satisfaction Problem (CSP)** optimization.

## Tech Stack

| Layer    | Technology                    |
|----------|-------------------------------|
| Frontend | React + Vite                  |
| Backend  | Python FastAPI                |
| Database | PostgreSQL (SQLAlchemy ORM)   |
| Algorithm| Custom CSP Solver             |

## Features

- **Automatic timetable generation** with conflict detection
- **Hard constraints**: No teacher/room/class double-booking
- **Soft constraints**: Gap minimization, load balancing
- **Fitness scoring** (0-100%) for timetable quality
- CRUD for Teachers, Subjects, Rooms, Classes
- Visual timetable grid with color-coded subject types
- Print/export support

## Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL

### Setup

```bash
# Windows
setup.bat

# Manual setup
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python -c "from backend.database.connection import engine, Base; from backend.models.models import *; Base.metadata.create_all(bind=engine)"
python database\seed.py

cd ../frontend
npm install
```

### Run

```bash
# Terminal 1 - Backend
cd backend
venv\Scripts\activate
uvicorn backend.main:app --reload

# Terminal 2 - Frontend
cd frontend
npm run dev
```

Open http://localhost:5173

## API Endpoints

| Method | Endpoint                     | Description              |
|--------|------------------------------|--------------------------|
| POST   | `/api/teachers`              | Add teacher              |
| GET    | `/api/teachers`              | List teachers            |
| POST   | `/api/subjects`              | Add subject              |
| GET    | `/api/subjects`              | List subjects            |
| POST   | `/api/rooms`                 | Add room                 |
| GET    | `/api/rooms`                 | List rooms               |
| POST   | `/api/classes`               | Add class                |
| GET    | `/api/classes`               | List classes             |
| POST   | `/api/timetable/generate`    | Generate timetable       |
| GET    | `/api/timetable/{id}`        | Get timetable by ID      |
| GET    | `/api/timetables`            | List all timetables      |

## Algorithm

The CSP solver works by:

1. Iterating over each class and its required subjects
2. Finding valid (teacher, room, day, period) combinations
3. Checking hard constraints:
   - No teacher double-booking
   - No room double-booking
   - No class double-booking
   - Lab subjects assigned to lab rooms
   - Teacher availability respected
4. Calculating fitness score: `100 - (conflict_penalty + gap_penalty + load_penalty)`
