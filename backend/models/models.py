from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
try:
    from backend.database.connection import Base
except ImportError:
    from database.connection import Base
import enum


class DayEnum(str, enum.Enum):
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"


class SubjectType(str, enum.Enum):
    THEORY = "theory"
    PRACTICAL = "practical"
    LAB = "lab"


class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    employee_id = Column(String(20), unique=True, nullable=False)
    email = Column(String(100))
    department = Column(String(50))

    subjects = relationship("Subject", back_populates="teacher")
    availabilities = relationship("TeacherAvailability", back_populates="teacher")
    lectures = relationship("Lecture", back_populates="teacher")


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    subject_type = Column(SQLEnum(SubjectType), default=SubjectType.THEORY)
    lectures_per_week = Column(Integer, nullable=False)
    requires_lab = Column(Boolean, default=False)

    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    teacher = relationship("Teacher", back_populates="subjects")
    lectures = relationship("Lecture", back_populates="subject")


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    room_number = Column(String(20), unique=True, nullable=False)
    capacity = Column(Integer, nullable=False)
    is_lab = Column(Boolean, default=False)

    lectures = relationship("Lecture", back_populates="room")


class TimeSlot(Base):
    __tablename__ = "time_slots"

    id = Column(Integer, primary_key=True, index=True)
    period_number = Column(Integer, nullable=False)
    start_time = Column(String(10), nullable=False)
    end_time = Column(String(10), nullable=False)

    lectures = relationship("Lecture", back_populates="time_slot")


class TeacherAvailability(Base):
    __tablename__ = "teacher_availability"

    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)
    day = Column(SQLEnum(DayEnum), nullable=False)
    period_number = Column(Integer, nullable=False)
    is_available = Column(Boolean, default=True)

    teacher = relationship("Teacher", back_populates="availabilities")


class ClassDivision(Base):
    __tablename__ = "class_divisions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    year = Column(Integer, nullable=False)
    section = Column(String(10), nullable=False)
    strength = Column(Integer, default=60)

    lectures = relationship("Lecture", back_populates="class_division")


class Lecture(Base):
    __tablename__ = "lectures"

    id = Column(Integer, primary_key=True, index=True)
    timetable_id = Column(Integer, ForeignKey("timetables.id", ondelete="CASCADE"))
    class_division_id = Column(Integer, ForeignKey("class_divisions.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    time_slot_id = Column(Integer, ForeignKey("time_slots.id"), nullable=False)
    day = Column(SQLEnum(DayEnum), nullable=False)

    class_division = relationship("ClassDivision", back_populates="lectures")
    subject = relationship("Subject", back_populates="lectures")
    teacher = relationship("Teacher", back_populates="lectures")
    room = relationship("Room", back_populates="lectures")
    time_slot = relationship("TimeSlot", back_populates="lectures")


class Timetable(Base):
    __tablename__ = "timetables"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    fitness_score = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(String(30))
