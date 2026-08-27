from typing import List, Dict, Tuple
from dataclasses import dataclass, field
from collections import defaultdict
import itertools


@dataclass
class ScheduleEntry:
    class_division_id: int
    subject_id: int
    teacher_id: int
    room_id: int
    day: str
    period: int
    subject_type: str = "theory"
    requires_lab: bool = False


@dataclass
class SchedulerInput:
    class_divisions: List[dict]
    subjects: List[dict]
    teachers: List[dict]
    rooms: List[dict]
    time_slots: List[dict]
    availability: List[dict]
    days: List[str] = field(default_factory=lambda: [
        "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"
    ])
    periods_per_day: int = 8


class TimetableCSP:
    def __init__(self, scheduler_input: SchedulerInput):
        self.input = scheduler_input
        self.schedule: List[ScheduleEntry] = []
        self.conflicts: List[dict] = []

    def _build_availability_map(self):
        amap = {}
        for a in self.input.availability:
            amap[(a["teacher_id"], a["day"], a["period_number"])] = a.get("is_available", True)
        return amap

    def _get_all_slots(self):
        slots = []
        for day in self.input.days:
            for period in range(1, self.input.periods_per_day + 1):
                slots.append((day, period))
        return slots

    def _get_teachers_for_subject(self, subject):
        tid = subject.get("teacher_id")
        return [t for t in self.input.teachers if t["id"] == tid]

    def _get_rooms_for_subject(self, subject, day, period, used_rooms):
        needs_lab = subject.get("requires_lab", False)
        valid = []
        for r in self.input.rooms:
            if r["id"] in used_rooms.get((day, period), set()):
                continue
            if needs_lab and not r.get("is_lab", False):
                continue
            valid.append(r)
        return valid

    def _get_all_subjects_for_class(self, cls):
        result = []
        for s in self.input.subjects:
            cid = s.get("class_division_id")
            if cid is None or cid == cls["id"]:
                result.append(s)
        return result

    def generate(self) -> Tuple[List[ScheduleEntry], int]:
        self.schedule = []
        self.conflicts = []

        avail_map = self._build_availability_map()
        all_slots = self._get_all_slots()

        used_teacher = set()
        used_room = set()
        used_class = set()

        for cls in self.input.class_divisions:
            subjects = self._get_all_subjects_for_class(cls)

            for subject in subjects:
                teachers = self._get_teachers_for_subject(subject)
                if not teachers:
                    self.conflicts.append({
                        "type": "no_teacher",
                        "message": f"No teacher for {subject['name']}",
                        "details": {"subject_id": subject["id"]},
                    })
                    continue

                teacher = teachers[0]
                needed = subject.get("lectures_per_week", 1)
                assigned = 0

                slots_shuffled = list(all_slots)
                for day, period in slots_shuffled:
                    if assigned >= needed:
                        break

                    t_key = (teacher["id"], day, period)
                    if t_key in used_teacher:
                        continue
                    if avail_map.get(t_key) is False:
                        continue

                    c_key = (cls["id"], day, period)
                    if c_key in used_class:
                        continue

                    rooms = self._get_rooms_for_subject(subject, day, period, self._used_room_by_slot(all_slots, used_room))
                    if not rooms:
                        continue

                    room = rooms[0]
                    r_key = (room["id"], day, period)
                    if r_key in used_room:
                        continue

                    entry = ScheduleEntry(
                        class_division_id=cls["id"],
                        subject_id=subject["id"],
                        teacher_id=teacher["id"],
                        room_id=room["id"],
                        day=day,
                        period=period,
                        subject_type=subject.get("subject_type", "theory"),
                        requires_lab=subject.get("requires_lab", False),
                    )
                    self.schedule.append(entry)
                    used_teacher.add(t_key)
                    used_room.add(r_key)
                    used_class.add(c_key)
                    assigned += 1

                if assigned < needed:
                    self.conflicts.append({
                        "type": "incomplete_schedule",
                        "message": f"{subject['name']} in {cls['name']}: needed {needed}, assigned {assigned}",
                        "details": {
                            "subject_id": subject["id"],
                            "class_id": cls["id"],
                            "needed": needed,
                            "assigned": assigned,
                        },
                    })

        fitness = self._calculate_fitness(used_teacher, used_class)
        return self.schedule, fitness

    def _used_room_by_slot(self, all_slots, used_room):
        result = defaultdict(set)
        for r_id, day, period in used_room:
            result[(day, period)].add(r_id)
        return result

    def _calculate_fitness(self, used_teacher, used_class) -> int:
        score = 100

        score -= len(self.conflicts) * 10

        teacher_days = defaultdict(lambda: defaultdict(int))
        for entry in self.schedule:
            teacher_days[entry.teacher_id][entry.day] += 1
        for tid, days in teacher_days.items():
            for day, count in days.items():
                if count > 4:
                    score -= 3

        class_gaps = 0
        class_periods = defaultdict(list)
        for entry in self.schedule:
            class_periods[(entry.class_division_id, entry.day)].append(entry.period)
        for key, periods in class_periods.items():
            sorted_p = sorted(periods)
            for i in range(len(sorted_p) - 1):
                if sorted_p[i + 1] - sorted_p[i] > 1:
                    class_gaps += 1
        score -= class_gaps * 2

        return max(0, min(100, score))

    def get_timetable_grid(self) -> Dict:
        grid = {}
        for entry in self.schedule:
            cls_id = entry.class_division_id
            if cls_id not in grid:
                grid[cls_id] = {}
            if entry.day not in grid[cls_id]:
                grid[cls_id][entry.day] = {}

            subject = next((s for s in self.input.subjects if s["id"] == entry.subject_id), None)
            teacher = next((t for t in self.input.teachers if t["id"] == entry.teacher_id), None)
            room = next((r for r in self.input.rooms if r["id"] == entry.room_id), None)

            grid[cls_id][entry.day][entry.period] = {
                "subject": subject["name"] if subject else "Unknown",
                "subject_code": subject.get("code", "") if subject else "",
                "teacher": teacher["name"] if teacher else "Unknown",
                "room": room["name"] if room else "Unknown",
                "subject_type": entry.subject_type,
            }

        return grid
