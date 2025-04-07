CREATE TABLE Staff (
    staff_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL
);

-- Courses Table
CREATE TABLE Courses (
    course_id INT PRIMARY KEY AUTO_INCREMENT,
    course_code VARCHAR(20) UNIQUE NOT NULL,
    course_name VARCHAR(255) NOT NULL,
    classes_per_week INT NOT NULL,
    eligible_teachers VARCHAR(255),
    FOREIGN KEY (eligible_teachers) REFERENCES Staff(staff_id)
);

-- Staff Preferred Courses Mapping
CREATE TABLE Staff_Courses (
    staff_id INT,
    course_id INT,
    PRIMARY KEY (staff_id, course_id),
    FOREIGN KEY (staff_id) REFERENCES Staff(staff_id),
    FOREIGN KEY (course_id) REFERENCES Courses(course_id)
);

-- Classes Table
CREATE TABLE Classes (
    class_id INT PRIMARY KEY AUTO_INCREMENT,
    degree VARCHAR(100) NOT NULL,
    semester INT NOT NULL,
    room_number VARCHAR(10) NOT NULL,
    block VARCHAR(50) NOT NULL
);

-- Class-Students Table
CREATE TABLE Class_Students (
    student_id INT,
    class_id INT,
    batch_number INT,
    PRIMARY KEY (student_id, class_id),
    FOREIGN KEY (class_id) REFERENCES Classes(class_id)
);

-- Course-Students Table
CREATE TABLE Course_Students (
    student_id INT,
    course_id INT,
    class_name VARCHAR(100) NOT NULL,
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (course_id) REFERENCES Courses(course_id)
);

-- Timetable Table
CREATE TABLE Timetable (
    timetable_id INT PRIMARY KEY AUTO_INCREMENT,
    day VARCHAR(20) NOT NULL,
    time_slot INT NOT NULL,
    course_id INT,
    staff_id INT,
    class_id INT,
    batch_number INT DEFAULT NULL,
    FOREIGN KEY (course_id) REFERENCES Courses(course_id),
    FOREIGN KEY (staff_id) REFERENCES Staff(staff_id),
    FOREIGN KEY (class_id) REFERENCES Classes(class_id)
);

-- Admin Requests Table
CREATE TABLE Admin_Requests (
    request_id INT PRIMARY KEY AUTO_INCREMENT,
    staff_id INT,
    requested_change TEXT NOT NULL,
    status ENUM('Pending', 'Approved', 'Rejected') DEFAULT 'Pending',
    FOREIGN KEY (staff_id) REFERENCES Staff(staff_id)
);

-- Holidays & Breaks Table
CREATE TABLE Holidays_Breaks (
    holiday_date DATE PRIMARY KEY,
    break_schedule TEXT NOT NULL
);
