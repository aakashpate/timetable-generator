from pydantic import BaseModel
from typing import Optional, List
from enum import Enum


class DayEnum(str, Enum):
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"


class SubjectType(str, Enum):
    THEORY = "theory"
    PRACTICAL = "practical"
    LAB = "lab"


class TeacherBase(BaseModel):
    name: str
    employee_id: str
    email: Optional[str] = None
    department: Optional[str] = None


class TeacherResponse(TeacherBase):
    id: int

    class Config:
        from_attributes = True


class SubjectBase(BaseModel):
    name: str
    code: str
    subject_type: SubjectType = SubjectType.THEORY
    lectures_per_week: int
    requires_lab: bool = False
    teacher_id: int


class SubjectResponse(SubjectBase):
    id: int

    class Config:
        from_attributes = True


class RoomBase(BaseModel):
    name: str
    room_number: str
    capacity: int
    is_lab: bool = False


class RoomResponse(RoomBase):
    id: int

    class Config:
        from_attributes = True


class TimeSlotBase(BaseModel):
    period_number: int
    start_time: str
    end_time: str


class TimeSlotResponse(TimeSlotBase):
    id: int

    class Config:
        from_attributes = True


class AvailabilityBase(BaseModel):
    teacher_id: int
    day: DayEnum
    period_number: int
    is_available: bool = True


class ClassDivisionBase(BaseModel):
    name: str
    year: int
    section: str
    strength: int = 60


class ClassDivisionResponse(ClassDivisionBase):
    id: int

    class Config:
        from_attributes = True


class LectureResponse(BaseModel):
    id: int
    class_division_id: int
    subject_id: int
    teacher_id: int
    room_id: int
    time_slot_id: int
    day: DayEnum
    subject_name: Optional[str] = None
    teacher_name: Optional[str] = None
    room_name: Optional[str] = None
    period_number: Optional[int] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None


class TimetableGenerateRequest(BaseModel):
    name: str


class TimetableResponse(BaseModel):
    id: int
    name: str
    fitness_score: int
    is_active: bool
    lectures: List[LectureResponse] = []


class ConflictInfo(BaseModel):
    type: str
    message: str
    details: dict


class FitnessScore(BaseModel):
    total: int
    hard_constraint_score: int
    soft_constraint_score: int
    conflicts: List[ConflictInfo] = []
