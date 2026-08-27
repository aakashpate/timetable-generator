from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
from typing import List, Dict
from datetime import datetime
import os

try:
    from backend.database.connection import engine, get_db, Base
    from backend.models.models import (
        Teacher, Subject, Room, TimeSlot, TeacherAvailability,
        ClassDivision, Lecture, Timetable
    )
    from backend.models.schemas import (
        TeacherBase, TeacherResponse,
        SubjectBase, SubjectResponse,
        RoomBase, RoomResponse,
        TimeSlotBase, TimeSlotResponse,
        AvailabilityBase, ClassDivisionBase, ClassDivisionResponse,
        LectureResponse, TimetableResponse, TimetableGenerateRequest,
        FitnessScore, ConflictInfo
    )
    from backend.scheduler.csp_solver import TimetableCSP, SchedulerInput
except ImportError:
    from database.connection import engine, get_db, Base
    from models.models import (
        Teacher, Subject, Room, TimeSlot, TeacherAvailability,
        ClassDivision, Lecture, Timetable
    )
    from models.schemas import (
        TeacherBase, TeacherResponse,
        SubjectBase, SubjectResponse,
        RoomBase, RoomResponse,
        TimeSlotBase, TimeSlotResponse,
        AvailabilityBase, ClassDivisionBase, ClassDivisionResponse,
        LectureResponse, TimetableResponse, TimetableGenerateRequest,
        FitnessScore, ConflictInfo
    )
    from scheduler.csp_solver import TimetableCSP, SchedulerInput


@asynccontextmanager
async def lifespan(app):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Timetable Generator API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Teacher Endpoints ---

@app.post("/api/teachers", response_model=TeacherResponse)
def create_teacher(teacher: TeacherBase, db: Session = Depends(get_db)):
    db_teacher = Teacher(**teacher.model_dump())
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher


@app.get("/api/teachers", response_model=List[TeacherResponse])
def get_teachers(db: Session = Depends(get_db)):
    return db.query(Teacher).all()


@app.get("/api/teachers/{teacher_id}", response_model=TeacherResponse)
def get_teacher(teacher_id: int, db: Session = Depends(get_db)):
    teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return teacher


@app.delete("/api/teachers/{teacher_id}")
def delete_teacher(teacher_id: int, db: Session = Depends(get_db)):
    teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    db.delete(teacher)
    db.commit()
    return {"message": "Teacher deleted"}


# --- Subject Endpoints ---

@app.post("/api/subjects", response_model=SubjectResponse)
def create_subject(subject: SubjectBase, db: Session = Depends(get_db)):
    db_subject = Subject(**subject.model_dump())
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject


@app.get("/api/subjects", response_model=List[SubjectResponse])
def get_subjects(db: Session = Depends(get_db)):
    return db.query(Subject).all()


@app.delete("/api/subjects/{subject_id}")
def delete_subject(subject_id: int, db: Session = Depends(get_db)):
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    db.delete(subject)
    db.commit()
    return {"message": "Subject deleted"}


# --- Room Endpoints ---

@app.post("/api/rooms", response_model=RoomResponse)
def create_room(room: RoomBase, db: Session = Depends(get_db)):
    db_room = Room(**room.model_dump())
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room


@app.get("/api/rooms", response_model=List[RoomResponse])
def get_rooms(db: Session = Depends(get_db)):
    return db.query(Room).all()


@app.delete("/api/rooms/{room_id}")
def delete_room(room_id: int, db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    db.delete(room)
    db.commit()
    return {"message": "Room deleted"}


# --- TimeSlot Endpoints ---

@app.post("/api/timeslots", response_model=TimeSlotResponse)
def create_timeslot(timeslot: TimeSlotBase, db: Session = Depends(get_db)):
    db_timeslot = TimeSlot(**timeslot.model_dump())
    db.add(db_timeslot)
    db.commit()
    db.refresh(db_timeslot)
    return db_timeslot


@app.get("/api/timeslots", response_model=List[TimeSlotResponse])
def get_timeslots(db: Session = Depends(get_db)):
    return db.query(TimeSlot).all()


# --- ClassDivision Endpoints ---

@app.post("/api/classes", response_model=ClassDivisionResponse)
def create_class(cls: ClassDivisionBase, db: Session = Depends(get_db)):
    db_cls = ClassDivision(**cls.model_dump())
    db.add(db_cls)
    db.commit()
    db.refresh(db_cls)
    return db_cls


@app.get("/api/classes", response_model=List[ClassDivisionResponse])
def get_classes(db: Session = Depends(get_db)):
    return db.query(ClassDivision).all()


@app.delete("/api/classes/{class_id}")
def delete_class(class_id: int, db: Session = Depends(get_db)):
    cls = db.query(ClassDivision).filter(ClassDivision.id == class_id).first()
    if not cls:
        raise HTTPException(status_code=404, detail="Class not found")
    db.delete(cls)
    db.commit()
    return {"message": "Class deleted"}


# --- Availability Endpoints ---

@app.post("/api/availability")
def create_availability(avail: AvailabilityBase, db: Session = Depends(get_db)):
    db_avail = TeacherAvailability(**avail.model_dump())
    db.add(db_avail)
    db.commit()
    return {"message": "Availability set"}


@app.get("/api/availability/{teacher_id}")
def get_availability(teacher_id: int, db: Session = Depends(get_db)):
    return db.query(TeacherAvailability).filter(
        TeacherAvailability.teacher_id == teacher_id
    ).all()


# --- Timetable Generation ---

@app.post("/api/timetable/generate")
def generate_timetable(request: TimetableGenerateRequest, db: Session = Depends(get_db)):
    teachers = db.query(Teacher).all()
    subjects = db.query(Subject).all()
    rooms = db.query(Room).all()
    time_slots = db.query(TimeSlot).all()
    classes = db.query(ClassDivision).all()
    availability = db.query(TeacherAvailability).all()

    if not teachers or not subjects or not rooms or not classes:
        raise HTTPException(
            status_code=400,
            detail="Insufficient data. Add teachers, subjects, rooms, and classes first."
        )

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    periods_per_day = len(time_slots) if time_slots else 8

    scheduler_input = SchedulerInput(
        class_divisions=[
            {"id": c.id, "name": c.name, "year": c.year, "section": c.section}
            for c in classes
        ],
        subjects=[
            {
                "id": s.id, "name": s.name, "code": s.code,
                "subject_type": s.subject_type.value,
                "lectures_per_week": s.lectures_per_week,
                "requires_lab": s.requires_lab,
                "teacher_id": s.teacher_id,
                "class_division_id": None,
            }
            for s in subjects
        ],
        teachers=[
            {"id": t.id, "name": t.name, "employee_id": t.employee_id}
            for t in teachers
        ],
        rooms=[
            {"id": r.id, "name": r.name, "room_number": r.room_number, "is_lab": r.is_lab}
            for r in rooms
        ],
        time_slots=[
            {"id": ts.id, "period_number": ts.period_number}
            for ts in time_slots
        ],
        availability=[
            {
                "teacher_id": a.teacher_id,
                "day": a.day.value,
                "period_number": a.period_number,
                "is_available": a.is_available,
            }
            for a in availability
        ],
        days=days,
        periods_per_day=periods_per_day,
    )

    csp = TimetableCSP(scheduler_input)
    schedule_entries, fitness_score = csp.generate()

    timetable = Timetable(
        name=request.name,
        fitness_score=fitness_score,
        is_active=True,
        created_at=datetime.now().isoformat(),
    )
    db.add(timetable)
    db.commit()
    db.refresh(timetable)

    time_slot_map = {ts.period_number: ts for ts in time_slots}
    subject_map = {s.id: s for s in subjects}
    teacher_map = {t.id: t for t in teachers}
    room_map = {r.id: r for r in rooms}

    lecture_responses = []
    for entry in schedule_entries:
        ts = time_slot_map.get(entry.period)
        lecture = Lecture(
            timetable_id=timetable.id,
            class_division_id=entry.class_division_id,
            subject_id=entry.subject_id,
            teacher_id=entry.teacher_id,
            room_id=entry.room_id,
            time_slot_id=ts.id if ts else 1,
            day=entry.day,
        )
        db.add(lecture)

        subj = subject_map.get(entry.subject_id)
        teach = teacher_map.get(entry.teacher_id)
        room = room_map.get(entry.room_id)

        lecture_responses.append(LectureResponse(
            id=0,
            class_division_id=entry.class_division_id,
            subject_id=entry.subject_id,
            teacher_id=entry.teacher_id,
            room_id=entry.room_id,
            time_slot_id=ts.id if ts else 1,
            day=entry.day,
            subject_name=subj.name if subj else "Unknown",
            teacher_name=teach.name if teach else "Unknown",
            room_name=room.name if room else "Unknown",
            period_number=entry.period,
            start_time=ts.start_time if ts else "",
            end_time=ts.end_time if ts else "",
        ))

    db.commit()

    return {
        "timetable": {
            "id": timetable.id,
            "name": timetable.name,
            "fitness_score": timetable.fitness_score,
        },
        "lectures": lecture_responses,
        "conflicts": csp.conflicts,
        "grid": csp.get_timetable_grid(),
    }


@app.get("/api/timetable/{timetable_id}")
def get_timetable(timetable_id: int, db: Session = Depends(get_db)):
    timetable = db.query(Timetable).filter(Timetable.id == timetable_id).first()
    if not timetable:
        raise HTTPException(status_code=404, detail="Timetable not found")

    lectures = db.query(Lecture).filter(Lecture.timetable_id == timetable_id).all()

    subject_map = {s.id: s for s in db.query(Subject).all()}
    teacher_map = {t.id: t for t in db.query(Teacher).all()}
    room_map = {r.id: r for r in db.query(Room).all()}
    ts_map = {ts.id: ts for ts in db.query(TimeSlot).all()}

    lecture_responses = []
    for lec in lectures:
        ts = ts_map.get(lec.time_slot_id)
        subj = subject_map.get(lec.subject_id)
        teach = teacher_map.get(lec.teacher_id)
        room = room_map.get(lec.room_id)

        lecture_responses.append(LectureResponse(
            id=lec.id,
            class_division_id=lec.class_division_id,
            subject_id=lec.subject_id,
            teacher_id=lec.teacher_id,
            room_id=lec.room_id,
            time_slot_id=lec.time_slot_id,
            day=lec.day.value if hasattr(lec.day, 'value') else lec.day,
            subject_name=subj.name if subj else "Unknown",
            teacher_name=teach.name if teach else "Unknown",
            room_name=room.name if room else "Unknown",
            period_number=ts.period_number if ts else 0,
            start_time=ts.start_time if ts else "",
            end_time=ts.end_time if ts else "",
        ))

    return {
        "id": timetable.id,
        "name": timetable.name,
        "fitness_score": timetable.fitness_score,
        "is_active": timetable.is_active,
        "lectures": lecture_responses,
    }


@app.get("/api/timetables")
def get_all_timetables(db: Session = Depends(get_db)):
    return db.query(Timetable).all()


@app.delete("/api/timetable/{timetable_id}")
def delete_timetable(timetable_id: int, db: Session = Depends(get_db)):
    timetable = db.query(Timetable).filter(Timetable.id == timetable_id).first()
    if not timetable:
        raise HTTPException(status_code=404, detail="Timetable not found")
    db.query(Lecture).filter(Lecture.timetable_id == timetable_id).delete()
    db.delete(timetable)
    db.commit()
    return {"message": "Timetable deleted"}


# --- Serve Frontend Static Files ---

FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend", "dist")

if os.path.exists(FRONTEND_DIR):
    app.mount("/assets", StaticFiles(directory=os.path.join(FRONTEND_DIR, "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        file_path = os.path.join(FRONTEND_DIR, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))
