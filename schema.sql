PRAGMA foreign_keys = OFF;

DROP TABLE IF EXISTS Tuition;
DROP TABLE IF EXISTS Registration;
DROP TABLE IF EXISTS Student_Degree;
DROP TABLE IF EXISTS Graduate;
DROP TABLE IF EXISTS Undergraduate;
DROP TABLE IF EXISTS Student_Major;
DROP TABLE IF EXISTS Student;
DROP TABLE IF EXISTS Instructor_Courses_Taught;
DROP TABLE IF EXISTS Instructor;
DROP TABLE IF EXISTS Section;
DROP TABLE IF EXISTS Course;
DROP TABLE IF EXISTS Department;

PRAGMA foreign_keys = ON;

-------------------------------------------------------
-- DEPARTMENT
-------------------------------------------------------
CREATE TABLE Department (
    Dept_ID INTEGER PRIMARY KEY,
    Department_Name TEXT NOT NULL,
    Department_Email TEXT,
    Department_Office TEXT
);

INSERT INTO Department VALUES
(1, 'Computer Science', 'cs@uni.ca', 'ENG-201'),
(2, 'Mathematics',     'math@uni.ca', 'SCI-101');

-------------------------------------------------------
-- COURSE
-------------------------------------------------------
CREATE TABLE Course (
    Dept_ID INTEGER,
    Course_ID INTEGER,
    Course_Name TEXT NOT NULL,
    Credits INTEGER,
    PRIMARY KEY (Dept_ID, Course_ID),
    FOREIGN KEY (Dept_ID) REFERENCES Department(Dept_ID)
);

INSERT INTO Course VALUES
(1, 101, 'Intro to Databases', 3),
(1, 102, 'Advanced SQL', 4),
(2, 201, 'Calculus I', 3);

-------------------------------------------------------
-- SECTION
-------------------------------------------------------
CREATE TABLE Section (
    Dept_ID INTEGER,
    Course_ID INTEGER,
    Section_No INTEGER,
    Instructor_Name TEXT,
    PRIMARY KEY (Dept_ID, Course_ID, Section_No),
    FOREIGN KEY (Dept_ID, Course_ID) REFERENCES Course(Dept_ID, Course_ID)
);

INSERT INTO Section VALUES
(1, 101, 1, 'Prof. Smith'),
(1, 102, 1, 'Prof. Post'),
(2, 201, 1, 'Prof. Peters');

-------------------------------------------------------
-- INSTRUCTOR
-------------------------------------------------------
CREATE TABLE Instructor (
    Instructor_ID INTEGER PRIMARY KEY,
    Instructor_Name TEXT NOT NULL,
    Instructor_Email TEXT
);

INSERT INTO Instructor VALUES
(1, 'Prof. Smith', 'smith@uni.ca'),
(2, 'Prof. Post',  'post@uni.ca'),
(3, 'Prof. Peters','peters@uni.ca');

-------------------------------------------------------
-- INSTRUCTOR COURSES TAUGHT
-------------------------------------------------------
CREATE TABLE Instructor_Courses_Taught (
    Instructor_ID INTEGER,
    Dept_ID INTEGER,
    Course_ID INTEGER,
    PRIMARY KEY (Instructor_ID, Dept_ID, Course_ID),
    FOREIGN KEY (Instructor_ID) REFERENCES Instructor(Instructor_ID),
    FOREIGN KEY (Dept_ID, Course_ID) REFERENCES Course(Dept_ID, Course_ID)
);

INSERT INTO Instructor_Courses_Taught VALUES
(1, 1, 101),
(2, 1, 102),
(3, 2, 201);

-------------------------------------------------------
-- STUDENT
-------------------------------------------------------
CREATE TABLE Student (
    Student_ID INTEGER PRIMARY KEY,
    First_Name TEXT NOT NULL,
    Last_Name TEXT NOT NULL,
    Email TEXT,
    DOB TEXT,
    Phone TEXT
);

INSERT INTO Student VALUES
(1001, 'Alice', 'Johnson', 'alice@uni.ca', '2000-01-15', '416-111-1111'),
(1002, 'Bob',   'Miller',  'bob@uni.ca',  '1999-05-20', '416-222-2222'),
(1003, 'Charlie','Brown',  'charlie@uni.ca','2001-09-10','416-333-3333');

-------------------------------------------------------
-- STUDENT MAJOR
-------------------------------------------------------
CREATE TABLE Student_Major (
    Student_ID INTEGER,
    Major_Name TEXT NOT NULL,
    PRIMARY KEY(Student_ID, Major_Name),
    FOREIGN KEY(Student_ID) REFERENCES Student(Student_ID)
);

INSERT INTO Student_Major VALUES
(1001, 'Computer Science'),
(1002, 'Mathematics'),
(1003, 'Computer Science');

-------------------------------------------------------
-- UNDERGRADUATE
-------------------------------------------------------
CREATE TABLE Undergraduate (
    Student_ID INTEGER PRIMARY KEY,
    Year_Level INTEGER,
    Expected_Grad_Year TEXT,
    FOREIGN KEY(Student_ID) REFERENCES Student(Student_ID)
);

INSERT INTO Undergraduate VALUES
(1001, 3, '2025'),
(1002, 2, '2026');

-------------------------------------------------------
-- GRADUATE
-------------------------------------------------------
CREATE TABLE Graduate (
    Student_ID INTEGER PRIMARY KEY,
    Degree_Type TEXT,
    Research_Area TEXT,
    Supervisor TEXT,
    FOREIGN KEY(Student_ID) REFERENCES Student(Student_ID)
);

INSERT INTO Graduate VALUES
(1003, 'Masters', 'Database Optimization', 'AI & Databases');

-------------------------------------------------------
-- STUDENT DEGREE
-------------------------------------------------------
CREATE TABLE Student_Degree (
    Student_ID INTEGER,
    Dept_ID INTEGER,
    Program_Name TEXT,
    Program_Type TEXT,
    University TEXT,
    PRIMARY KEY(Student_ID, Dept_ID, Program_Name),
    FOREIGN KEY(Student_ID) REFERENCES Student(Student_ID),
    FOREIGN KEY(Dept_ID) REFERENCES Department(Dept_ID)
);

INSERT INTO Student_Degree VALUES
(1001, 1, 'B.C.S', 'Bachelor', 'TMU'),
(1002, 1, 'B.A',   'Bachelor', 'TMU'),
(1003, 1, 'B.C.S', 'Bachelor', 'TMU');

-------------------------------------------------------
-- REGISTRATION
-------------------------------------------------------
CREATE TABLE Registration (
    Registration_ID INTEGER PRIMARY KEY,
    Student_ID INTEGER,
    Dept_ID INTEGER,
    Course_ID INTEGER,
    Section_No INTEGER,
    FOREIGN KEY(Student_ID) REFERENCES Student(Student_ID),
    FOREIGN KEY(Dept_ID, Course_ID, Section_No) REFERENCES Section(Dept_ID, Course_ID, Section_No)
);

INSERT INTO Registration VALUES
(5001, 1001, 1, 101, 1),
(5002, 1002, 1, 102, 1),
(5003, 1003, 2, 201, 1);

-------------------------------------------------------
-- TUITION
-------------------------------------------------------
CREATE TABLE Tuition (
    Student_ID INTEGER,
    Dept_ID INTEGER,
    Payment_Deadline TEXT,
    Payment_Amount INTEGER,
    Payment_Status TEXT,
    PRIMARY KEY(Student_ID, Dept_ID),
    FOREIGN KEY(Student_ID) REFERENCES Student(Student_ID),
    FOREIGN KEY(Dept_ID) REFERENCES Department(Dept_ID)
);

INSERT INTO Tuition VALUES
(1001, 1, '2025-09-30', 5000, 'Paid'),
(1002, 1, '2025-09-30', 4800, 'Unpaid'),
(1003, 1, '2025-09-30', 5200, 'Paid');
