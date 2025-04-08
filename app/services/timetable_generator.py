from app.models import db
from app.models.timetable_model import Timetable
from app.models.class_model import Classes
from app.models.course_model import Courses, CourseStaff
from app.models.staff_model import Staff
from typing import Dict, List, Set, Tuple
import random

class TimetableGenerator:
    def __init__(self):
        self.total_days = 5
        self.periods_per_day = 7
        self.occupied_slots = {}  # (day, period) -> set of staff_ids
        self.staff_schedule = {}  # staff_id -> set of (day, period)
        self.room_schedule = {}   # room -> set of (day, period)
        self.max_hours_per_day = 6  # Maximum teaching hours per day for staff

    def generate(self):
        """Main generation method with all constraints"""
        try:
            # Clear existing timetable
            db.session.query(Timetable).delete()
            db.session.commit()

            # Get all required data
            classes = Classes.query.all()
            courses = Courses.query.all()
            staff = Staff.query.all()

            for cls in classes:
                self._generate_class_timetable(cls, courses, staff)

            return True, "Timetable generated successfully"
        except Exception as e:
            db.session.rollback()
            return False, str(e)

    def _generate_class_timetable(self, cls: Classes, courses: List[Courses], staff: List[Staff]):
        """Generate timetable for a specific class"""
        
        # Initialize tracking for this class
        class_slots = set()
        remaining_courses = self._get_courses_with_hours(courses)

        # Handle fixed slots first (e.g., Wednesday afternoon academic slot)
        self._assign_fixed_slots(cls)

        # Handle lab sessions (they need continuous periods)
        lab_courses = [c for c in courses if self._is_lab_course(c)]
        for lab in lab_courses:
            self._assign_lab_slots(cls, lab, remaining_courses)

        # Assign regular classes
        for day in range(self.total_days):
            for period in range(self.periods_per_day):
                if not self._is_valid_period(cls, day, period):
                    continue

                if not remaining_courses:
                    continue

                # Find suitable course and teacher
                course, teacher = self._find_suitable_assignment(
                    cls, day, period, remaining_courses, staff
                )

                if course and teacher:
                    # Create timetable entry
                    entry = Timetable(
                        class_id=cls.class_id,
                        day=day,
                        period=period,
                        course_id=course.course_id,
                        staff_id=teacher.staff_id
                    )
                    db.session.add(entry)
                    
                    # Update tracking
                    self._update_schedules(cls, course, teacher, day, period)
                    remaining_courses[course] -= 1
                    if remaining_courses[course] == 0:
                        del remaining_courses[course]

        db.session.commit()

    def _is_teacher_available(self, teacher_id: int, day: int, period: int) -> bool:
        # Check if teacher has reached max hours for the day
        day_slots = sum(1 for d, p in self.staff_schedule.get(teacher_id, set()) 
                       if d == day)
        if day_slots >= self.max_hours_per_day:
            return False
            
        return (day, period) not in self.staff_schedule.get(teacher_id, set())

    def _is_room_available(self, room: str, day: int, period: int) -> bool:
        return (day, period) not in self.room_schedule.get(room, set())

    def _is_valid_period(self, cls: Classes, day: int, period: int) -> bool:
        """Enhanced period validation"""
        # Break periods (different for first years)
        if cls.semester == 1:
            if period in [2, 4]:  # Break and lunch for first years
                return False
        else:
            if period in [3, 5]:  # Break and lunch for other years
                return False

        # No classes on Wednesday afternoon (academic slot)
        if day == 2 and period >= 4:
            return False

        return True

    def _find_suitable_assignment(
        self, cls: Classes, day: int, period: int, 
        remaining_courses: Dict[Courses, int], staff: List[Staff]
    ) -> Tuple[Courses, Staff]:
        """Find suitable course and teacher for a slot"""
        for course, hours in remaining_courses.items():
            if hours <= 0:
                continue

            # Get eligible teachers
            eligible_teachers = self._get_eligible_teachers(course, staff)
            random.shuffle(eligible_teachers)  # Randomize for better distribution

            for teacher in eligible_teachers:
                if self._can_assign(cls, course, teacher, day, period):
                    return course, teacher

        return None, None

    def _can_assign(
        self, cls: Classes, course: Courses, 
        teacher: Staff, day: int, period: int
    ) -> bool:
        """Check if assignment is possible with all constraints"""
        slot_key = f"{day}_{period}"
        teacher_key = f"{teacher.staff_id}_{slot_key}"
        class_key = f"{cls.class_id}_{slot_key}"
        room_key = f"{cls.default_room}_{slot_key}"

        return not (
            teacher_key in self.staff_schedule or
            class_key in self.occupied_slots or
            room_key in self.room_schedule
        )

    # Helper methods...
    def _get_courses_with_hours(self, courses: List[Courses]) -> Dict[Courses, int]:
        return {course: course.classes_per_week for course in courses}

    def _get_eligible_teachers(self, course: Courses, staff: List[Staff]) -> List[Staff]:
        eligible_ids = CourseStaff.query.filter_by(course_id=course.course_id).all()
        return [s for s in staff if s.staff_id in [e.staff_id for e in eligible_ids]]

    def _is_lab_course(self, course: Courses) -> bool:
        """Check if course is a lab course based on name/code"""
        return 'lab' in course.course_name.lower() or 'practical' in course.course_name.lower()

    def _assign_lab_slots(self, cls: Classes, lab: Courses, remaining_courses: Dict[Courses, int]):
        """Assign lab slots (needs continuous periods)"""
        lab_periods = 2  # Standard lab duration
        for day in range(self.total_days):
            # Try to find continuous slots
            for start_period in range(self.periods_per_day - lab_periods + 1):
                if all(self._is_valid_period(cls, day, p) for p in range(start_period, start_period + lab_periods)):
                    # Found valid slot block
                    teacher = self._get_lab_teacher(lab)
                    if teacher:
                        self._assign_lab_block(cls, lab, teacher, day, start_period, lab_periods)
                        remaining_courses[lab] -= lab_periods
                        if remaining_courses[lab] <= 0:
                            del remaining_courses[lab]
                        break

    def _get_lab_teacher(self, lab: Courses) -> Staff:
        """Get available lab teacher"""
        eligible_staff = CourseStaff.query.filter_by(course_id=lab.course_id).all()
        return Staff.query.filter(Staff.staff_id.in_([s.staff_id for s in eligible_staff])).first()

    def _assign_lab_block(self, cls: Classes, lab: Courses, teacher: Staff, day: int, start_period: int, duration: int):
        """Assign a block of periods for lab"""
        for period in range(start_period, start_period + duration):
            entry = Timetable(
                class_id=cls.class_id,
                day=day,
                period=period,
                course_id=lab.course_id,
                staff_id=teacher.staff_id,
                is_lab=True
            )
            db.session.add(entry)
            self._update_schedules(cls, lab, teacher, day, period)
