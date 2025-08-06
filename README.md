# 📅 Timetable Generator – DBMS Project

A Flask + MySQL-based **automated timetable generation system** designed to create clash-free class schedules for universities.  
It incorporates teacher preferences, batch-wise labs, fixed activities, and holiday rules while allowing admins full control over modifications.

---

## 🚀 Features

- **Automated Timetable Generation**
  - Prevents clashes between courses, teachers, and rooms.
  - Supports **multiple semesters** and **multiple classes** at once.

- **Teacher Preferences**
  - Teachers can set preferred courses and classes before timetable generation.

- **Batch-Wise Labs**
  - Labs are scheduled in **2–3 continuous hours** for each batch.
  - Each batch has separate lab rooms.

- **Self-Learning Slots**
  - Fixed per week, evenly distributed, configurable by admin.

- **Fixed Rules & Constraints**
  - Sundays are holidays.
  - Break timings differ for first-year vs other students.
  - Certain slots are fixed (e.g., activity periods on Wednesday).

- **Room Assignments**
  - Each class has a fixed room; labs/joint classes have dedicated rooms.

- **Admin Panel**
  - Full control to override schedules.
  - Approves mid-semester change requests from professors.

---

## 🛠 Tech Stack

- **Backend:** Python, Flask, SQLAlchemy
- **Database:** MySQL
- **Frontend:** HTML, CSS, JavaScript
- **Authentication:** Dummy login system (future: Microsoft 365 API)

---

## 📂 Database Design

### Tables
1. **Staff**
   - `staff_id` (PK)
   - `name`
   - `preferred_courses` (FK → Courses)

2. **Courses**
   - `course_id` (PK)
   - `course_code`
   - `course_name`
   - `classes_per_week`
   - `eligible_teachers` (FK → Staff)

3. **Classes**
   - `class_id` (PK)
   - `class_name`
   - `degree`
   - `semester`
   - `room_number`

4. **Class_Students**
   - `student_id` (PK)
   - `class_id` (FK → Classes)
   - `batch_number`

5. **Course_Students**
   - `id` (PK)
   - `course_id` (FK → Courses)
   - `student_id` (FK → Class_Students)
   - `class_name`

---

## 📋 Timetable Rules

- **Format:** Day × Session table.
- **Display:** Course code in cells, legend below with professor initials & names.
- **Breaks:**
  - **1st Year:** Break after 2nd hour, lunch after 4th hour.
  - **Others:** Break after 3rd hour, lunch after 5th hour.
- **Labs:** 2–3 continuous slots, batch-separated.
- **Holidays:** Sunday fixed, other holidays configurable.

---

## ⚙️ Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/timetable-generator.git
   cd timetable-generator





