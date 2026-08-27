"""Seed the database with sample data."""
from database.connection import engine, SessionLocal, Base
from models.models import Teacher, Subject, Room, TimeSlot, ClassDivision


def seed_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    if db.query(Teacher).count() > 0:
        print("Database already seeded. Skipping.")
        db.close()
        return

    for p, s, e in [
        (1, "08:00", "08:50"), (2, "09:00", "09:50"), (3, "10:00", "10:50"),
        (4, "11:00", "11:50"), (5, "12:00", "12:50"), (6, "14:00", "14:50"),
        (7, "15:00", "15:50"), (8, "16:00", "16:50"),
    ]:
        db.add(TimeSlot(period_number=p, start_time=s, end_time=e))

    for name, eid, email, dept in [
        ("Dr. Ramesh Kumar", "T001", "ramesh@school.edu", "Mathematics"),
        ("Prof. Sunita Sharma", "T002", "sunita@school.edu", "Physics"),
        ("Mr. Amit Patel", "T003", "amit@school.edu", "Chemistry"),
        ("Mrs. Priya Desai", "T004", "priya@school.edu", "English"),
        ("Dr. Vikram Singh", "T005", "vikram@school.edu", "Computer Science"),
        ("Ms. Neha Gupta", "T006", "neha@school.edu", "Biology"),
    ]:
        db.add(Teacher(name=name, employee_id=eid, email=email, department=dept))
    db.flush()

    for name, code, stype, lpw, lab, tid in [
        ("Mathematics", "MATH101", "theory", 5, False, 1),
        ("Physics", "PHY101", "theory", 4, False, 2),
        ("Physics Lab", "PHY101L", "lab", 1, True, 2),
        ("Chemistry", "CHM101", "theory", 4, False, 3),
        ("Chemistry Lab", "CHM101L", "lab", 1, True, 3),
        ("English", "ENG101", "theory", 4, False, 4),
        ("Computer Science", "CS101", "theory", 3, False, 5),
        ("CS Lab", "CS101L", "lab", 2, True, 5),
        ("Biology", "BIO101", "theory", 3, False, 6),
    ]:
        db.add(Subject(name=name, code=code, subject_type=stype, lectures_per_week=lpw, requires_lab=lab, teacher_id=tid))

    for name, rnum, cap, is_lab in [
        ("Room 101", "R101", 60, False), ("Room 102", "R102", 60, False),
        ("Room 103", "R103", 40, False), ("Physics Lab", "PL01", 30, True),
        ("Chemistry Lab", "CL01", 30, True), ("CS Lab", "CSL01", 30, True),
        ("Room 201", "R201", 60, False), ("Room 202", "R202", 40, False),
    ]:
        db.add(Room(name=name, room_number=rnum, capacity=cap, is_lab=is_lab))

    for name, year, sec, strength in [
        ("Class 10-A", 10, "A", 45), ("Class 10-B", 10, "B", 42), ("Class 11-A", 11, "A", 40),
    ]:
        db.add(ClassDivision(name=name, year=year, section=sec, strength=strength))

    db.commit()
    db.close()
    print("Database seeded successfully!")


if __name__ == "__main__":
    seed_db()
