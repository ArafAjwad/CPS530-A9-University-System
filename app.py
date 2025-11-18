from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "supersecretkey"   # Required for flash messages


# ---------------------------------------------------------
# DATABASE CONNECTION
# ---------------------------------------------------------
def get_db_connection():
    conn = sqlite3.connect("university.db")
    conn.row_factory = sqlite3.Row
    return conn


# ---------------------------------------------------------
# HOME PAGE
# ---------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html", title="University App")
# ---------------------------------------------------------
# STUDENTS - LIST
# ---------------------------------------------------------
@app.route("/students")
def students():
    conn = get_db_connection()
    students = conn.execute("SELECT * FROM Student").fetchall()
    conn.close()
    return render_template("students.html", title="Students", students=students)


# ---------------------------------------------------------
# STUDENTS - ADD
# ---------------------------------------------------------
@app.route("/add-student", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        first = request.form["first_name"]
        last = request.form["last_name"]
        email = request.form["email"]
        dob = request.form["dob"]
        phone = request.form["phone"]

        conn = get_db_connection()
        conn.execute("""
            INSERT INTO Student (Student_ID, First_Name, Last_Name, Email, DOB, Phone)
            VALUES ((SELECT COALESCE(MAX(Student_ID), 1000) + 1 FROM Student),
                    ?,?,?,?,?)
        """, (first, last, email, dob, phone))
        conn.commit()
        conn.close()

        flash("Student added successfully!", "success")
        return redirect(url_for("students"))

    return render_template("add_student.html", title="Add Student")


# ---------------------------------------------------------
# STUDENTS - UPDATE
# ---------------------------------------------------------
@app.route("/update-student/<int:id>", methods=["GET", "POST"])
def update_student(id):
    conn = get_db_connection()
    
    student = conn.execute("SELECT * FROM Student WHERE Student_ID = ?", (id,)).fetchone()
    
    if not student:
        flash("Student not found!", "danger")
        return redirect(url_for("students"))

    if request.method == "POST":
        first = request.form["first_name"]
        last = request.form["last_name"]
        email = request.form["email"]
        dob = request.form["dob"]
        phone = request.form["phone"]

        conn.execute("""
            UPDATE Student
            SET First_Name = ?, Last_Name = ?, Email = ?, DOB = ?, Phone = ?
            WHERE Student_ID = ?
        """, (first, last, email, dob, phone, id))
        conn.commit()
        conn.close()

        flash("Student updated successfully!", "success")
        return redirect(url_for("students"))

    return render_template("update_student.html", title="Update Student", student=student)

# ---------------------------------------------------------
# STUDENTS - DELETE   
# ---------------------------------------------------------
@app.route("/delete-student/<int:id>")
def delete_student(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM Student WHERE Student_ID = ?", (id,))
    conn.commit()
    conn.close()

    flash("Student deleted successfully!", "success")
    return redirect(url_for("students"))

# ---------------------------------------------------------
# STUDENTS - SEARCH
# ---------------------------------------------------------
@app.route("/search-students")
def search_students():
    q = request.args.get("query", "").strip()

    conn = get_db_connection()
    results = conn.execute("""
        SELECT * FROM Student
        WHERE 
            Student_ID LIKE ? OR
            First_Name LIKE ? OR
            Last_Name LIKE ?
    """, (f"%{q}%", f"%{q}%", f"%{q}%")).fetchall()
    conn.close()

    return render_template(
        "students.html",
        title=f"Search Results for '{q}'",
        students=results
    )

# ---------------------------------------------------------
# DEPARTMENTS - LIST
# ---------------------------------------------------------
@app.route("/departments")
def departments():
    conn = get_db_connection()
    depts = conn.execute("SELECT * FROM Department").fetchall()
    conn.close()
    return render_template("departments.html", title="Departments", departments=depts)
# ---------------------------------------------------------
# DEPARTMENTS - ADD
# ---------------------------------------------------------
@app.route("/add-department", methods=["GET", "POST"])
def add_department():
    if request.method == "POST":
        dept_name = request.form["department_name"]
        dept_email = request.form["department_email"]
        dept_office = request.form["department_office"]

        conn = get_db_connection()
        conn.execute("""
            INSERT INTO Department (Dept_ID, Department_Name, Department_Email, Department_Office)
            VALUES (
                (SELECT COALESCE(MAX(Dept_ID), 0) + 1 FROM Department),
                ?, ?, ?
            )
        """, (dept_name, dept_email, dept_office))
        conn.commit()
        conn.close()

        flash("Department added successfully!", "success")
        return redirect(url_for("departments"))

    return render_template("add_department.html", title="Add Department")
# ---------------------------------------------------------
# DEPARTMENTS - UPDATE
# ---------------------------------------------------------
@app.route("/update-department/<int:id>", methods=["GET", "POST"])
def update_department(id):
    conn = get_db_connection()
    dept = conn.execute("SELECT * FROM Department WHERE Dept_ID = ?", (id,)).fetchone()

    if not dept:
        flash("Department not found!", "danger")
        return redirect(url_for("departments"))

    if request.method == "POST":
        dept_name = request.form["department_name"]
        dept_email = request.form["department_email"]
        dept_office = request.form["department_office"]

        conn.execute("""
            UPDATE Department
            SET Department_Name = ?, Department_Email = ?, Department_Office = ?
            WHERE Dept_ID = ?
        """, (dept_name, dept_email, dept_office, id))
        conn.commit()
        conn.close()

        flash("Department updated successfully!", "success")
        return redirect(url_for("departments"))

    return render_template("update_department.html", title="Update Department", dept=dept)
# ---------------------------------------------------------
# COURSES - LIST
# ---------------------------------------------------------
@app.route("/courses")
def courses():
    conn = get_db_connection()
    courses = conn.execute("SELECT * FROM Course").fetchall()
    conn.close()

    return render_template("courses.html", title="Courses", courses=courses)
# ---------------------------------------------------------
# COURSES - ADD
# ---------------------------------------------------------
@app.route("/add-course", methods=["GET", "POST"])
def add_course():
    if request.method == "POST":
        dept_id = request.form["dept_id"]
        course_id = request.form["course_id"]
        course_name = request.form["course_name"]
        credits = request.form["credits"]

        conn = get_db_connection()
        conn.execute("""
            INSERT INTO Course (Dept_ID, Course_ID, Course_Name, Credits)
            VALUES (?, ?, ?, ?)
        """, (dept_id, course_id, course_name, credits))
        conn.commit()
        conn.close()

        flash("Course added successfully!", "success")
        return redirect(url_for("courses"))

    return render_template("add_course.html", title="Add Course")
# ---------------------------------------------------------
# COURSES - UPDATE
# ---------------------------------------------------------
@app.route("/update-course/<int:dept>/<int:course>", methods=["GET", "POST"])
def update_course(dept, course):
    conn = get_db_connection()
    c = conn.execute(
        "SELECT * FROM Course WHERE Dept_ID = ? AND Course_ID = ?",
        (dept, course)
    ).fetchone()

    if not c:
        flash("Course not found!", "danger")
        return redirect(url_for("courses"))

    if request.method == "POST":
        dept_id = request.form["dept_id"]
        course_id = request.form["course_id"]
        course_name = request.form["course_name"]
        credits = request.form["credits"]

        conn.execute("""
            UPDATE Course
            SET Dept_ID = ?, Course_ID = ?, Course_Name = ?, Credits = ?
            WHERE Dept_ID = ? AND Course_ID = ?
        """, (dept_id, course_id, course_name, credits, dept, course))
        conn.commit()
        conn.close()

        flash("Course updated successfully!", "success")
        return redirect(url_for("courses"))

    return render_template("update_course.html", title="Update Course", course=c)
# ---------------------------------------------------------
# SECTIONS - LIST
# ---------------------------------------------------------
@app.route("/sections")
def sections():
    conn = get_db_connection()
    sections = conn.execute("SELECT * FROM Section").fetchall()
    conn.close()

    return render_template("sections.html", title="Sections", sections=sections)
# ---------------------------------------------------------
# SECTIONS - ADD
# ---------------------------------------------------------
@app.route("/add-section", methods=["GET", "POST"])
def add_section():
    if request.method == "POST":
        dept_id = request.form["dept_id"]
        course_id = request.form["course_id"]
        section_no = request.form["section_no"]
        instructor_name = request.form["instructor_name"]

        conn = get_db_connection()
        conn.execute("""
            INSERT INTO Section (Dept_ID, Course_ID, Section_No, Instructor_Name)
            VALUES (?, ?, ?, ?)
        """, (dept_id, course_id, section_no, instructor_name))
        conn.commit()
        conn.close()

        flash("Section added successfully!", "success")
        return redirect(url_for("sections"))

    return render_template("add_section.html", title="Add Section")
# ---------------------------------------------------------
# SECTIONS - UPDATE
# ---------------------------------------------------------
@app.route("/update-section/<int:dept>/<int:course>/<int:section>", methods=["GET", "POST"])
def update_section(dept, course, section):
    conn = get_db_connection()
    sec = conn.execute("""
        SELECT * FROM Section
        WHERE Dept_ID = ? AND Course_ID = ? AND Section_No = ?
    """, (dept, course, section)).fetchone()

    if not sec:
        flash("Section not found!", "danger")
        return redirect(url_for("sections"))

    if request.method == "POST":
        dept_id = request.form["dept_id"]
        course_id = request.form["course_id"]
        section_no = request.form["section_no"]
        instructor_name = request.form["instructor_name"]

        conn.execute("""
            UPDATE Section
            SET Dept_ID = ?, Course_ID = ?, Section_No = ?, Instructor_Name = ?
            WHERE Dept_ID = ? AND Course_ID = ? AND Section_No = ?
        """, (dept_id, course_id, section_no, instructor_name, dept, course, section))
        conn.commit()
        conn.close()

        flash("Section updated successfully!", "success")
        return redirect(url_for("sections"))

    return render_template("update_section.html", title="Update Section", sec=sec)
# ---------------------------------------------------------
# INSTRUCTORS - LIST
# ---------------------------------------------------------
@app.route("/instructors")
def instructors():
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM Instructor").fetchall()
    conn.close()

    return render_template(
        "instructors.html",
        title="Instructors",
        instructors=rows
    )
# ---------------------------------------------------------
# INSTRUCTORS - ADD
# ---------------------------------------------------------
@app.route("/add-instructor", methods=["GET", "POST"])
def add_instructor():
    if request.method == "POST":
        name = request.form["instructor_name"]
        email = request.form["instructor_email"]

        conn = get_db_connection()
        conn.execute("""
            INSERT INTO Instructor (Instructor_ID, Instructor_Name, Instructor_Email)
            VALUES ((SELECT COALESCE(MAX(Instructor_ID), 0) + 1 FROM Instructor),
                    ?, ?)
        """, (name, email))
        conn.commit()
        conn.close()

        flash("Instructor added successfully!", "success")
        return redirect(url_for("instructors"))

    return render_template(
        "add_instructor.html",
        title="Add Instructor"
    )
# ---------------------------------------------------------
# INSTRUCTORS - UPDATE
# ---------------------------------------------------------
@app.route("/update-instructor/<int:id>", methods=["GET", "POST"])
def update_instructor(id):
    conn = get_db_connection()
    ins = conn.execute(
        "SELECT * FROM Instructor WHERE Instructor_ID = ?",
        (id,)
    ).fetchone()

    if not ins:
        flash("Instructor not found!", "danger")
        return redirect(url_for("instructors"))

    if request.method == "POST":
        name = request.form["instructor_name"]
        email = request.form["instructor_email"]

        conn.execute("""
            UPDATE Instructor
            SET Instructor_Name = ?, Instructor_Email = ?
            WHERE Instructor_ID = ?
        """, (name, email, id))
        conn.commit()
        conn.close()

        flash("Instructor updated successfully!", "success")
        return redirect(url_for("instructors"))

    return render_template(
        "update_instructor.html",
        title="Update Instructor",
        instructor=ins
    )
# ---------------------------------------------------------
# ICT - LIST
# ---------------------------------------------------------
@app.route("/ict")
def ict():
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM Instructor_Courses_Taught").fetchall()
    conn.close()

    return render_template(
        "ict.html",
        title="Instructor Courses Taught",
        ict=rows
    )
# ---------------------------------------------------------
# ICT - ADD
# ---------------------------------------------------------
@app.route("/add-ict", methods=["GET", "POST"])
def add_ict():
    if request.method == "POST":
        instructor_id = request.form["instructor_id"]
        dept_id = request.form["dept_id"]
        course_id = request.form["course_id"]

        conn = get_db_connection()
        conn.execute("""
            INSERT INTO Instructor_Courses_Taught (Instructor_ID, Dept_ID, Course_ID)
            VALUES (?, ?, ?)
        """, (instructor_id, dept_id, course_id))
        conn.commit()
        conn.close()

        flash("Instructor Course Taught added successfully!", "success")
        return redirect(url_for("ict"))

    return render_template(
        "add_ict.html",
        title="Add Instructor Course Taught"
    )
# ---------------------------------------------------------
# ICT - UPDATE
# ---------------------------------------------------------
@app.route("/update-ict/<int:i_id>/<int:d_id>/<int:c_id>", methods=["GET", "POST"])
def update_ict(i_id, d_id, c_id):
    conn = get_db_connection()
    row = conn.execute("""
        SELECT * FROM Instructor_Courses_Taught
        WHERE Instructor_ID = ? AND Dept_ID = ? AND Course_ID = ?
    """, (i_id, d_id, c_id)).fetchone()

    if not row:
        flash("Record not found!", "danger")
        return redirect(url_for("ict"))

    if request.method == "POST":
        new_instructor_id = request.form["instructor_id"]
        new_dept_id = request.form["dept_id"]
        new_course_id = request.form["course_id"]

        conn.execute("""
            UPDATE Instructor_Courses_Taught
            SET Instructor_ID = ?, Dept_ID = ?, Course_ID = ?
            WHERE Instructor_ID = ? AND Dept_ID = ? AND Course_ID = ?
        """, (
            new_instructor_id, new_dept_id, new_course_id,
            i_id, d_id, c_id
        ))
        conn.commit()
        conn.close()

        flash("Instructor Course Taught updated successfully!", "success")
        return redirect(url_for("ict"))

    return render_template(
        "update_ict.html",
        title="Update Instructor Course Taught",
        row=row
    )
# ---------------------------------------------------------
# STUDENT MAJOR - LIST
# ---------------------------------------------------------
@app.route("/student-majors")
def student_majors():
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM Student_Major").fetchall()
    conn.close()

    return render_template(
        "student_majors.html",
        title="Student Majors",
        majors=rows
    )
# ---------------------------------------------------------
# STUDENT MAJOR - ADD
# ---------------------------------------------------------
@app.route("/add-student-major", methods=["GET", "POST"])
def add_student_major():
    if request.method == "POST":
        student_id = request.form["student_id"]
        major_name = request.form["major_name"]

        conn = get_db_connection()
        conn.execute("""
            INSERT INTO Student_Major (Student_ID, Major_Name)
            VALUES (?, ?)
        """, (student_id, major_name))
        conn.commit()
        conn.close()

        flash("Student Major added successfully!", "success")
        return redirect(url_for("student_majors"))

    return render_template(
        "add_student_major.html",
        title="Add Student Major"
    )
# ---------------------------------------------------------
# STUDENT MAJOR - UPDATE
# ---------------------------------------------------------
@app.route("/update-student-major/<int:s_id>/<major>", methods=["GET", "POST"])
def update_student_major(s_id, major):
    conn = get_db_connection()
    row = conn.execute("""
        SELECT * FROM Student_Major
        WHERE Student_ID = ? AND Major_Name = ?
    """, (s_id, major)).fetchone()

    if not row:
        flash("Record not found!", "danger")
        return redirect(url_for("student_majors"))

    if request.method == "POST":
        new_student_id = request.form["student_id"]
        new_major_name = request.form["major_name"]

        conn.execute("""
            UPDATE Student_Major
            SET Student_ID = ?, Major_Name = ?
            WHERE Student_ID = ? AND Major_Name = ?
        """, (new_student_id, new_major_name, s_id, major))
        conn.commit()
        conn.close()

        flash("Student Major updated successfully!", "success")
        return redirect(url_for("student_majors"))

    return render_template(
        "update_student_major.html",
        title="Update Student Major",
        major=row
    )
# ---------------------------------------------------------
# UNDERGRADUATE - LIST
# ---------------------------------------------------------
@app.route("/undergraduate")
def undergraduate():
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM Undergraduate").fetchall()
    conn.close()

    return render_template(
        "undergraduate.html",
        title="Undergraduate Students",
        undergrad=rows
    )
# ---------------------------------------------------------
# UNDERGRADUATE - ADD
# ---------------------------------------------------------
@app.route("/add-undergraduate", methods=["GET", "POST"])
def add_undergraduate():
    if request.method == "POST":
        student_id = request.form["student_id"]
        year_level = request.form["year_level"]
        grad_year = request.form["expected_grad_year"]

        conn = get_db_connection()
        conn.execute("""
            INSERT INTO Undergraduate (Student_ID, Year_Level, Expected_Grad_Year)
            VALUES (?, ?, ?)
        """, (student_id, year_level, grad_year))
        conn.commit()
        conn.close()

        flash("Undergraduate record added!", "success")
        return redirect(url_for("undergraduate"))

    return render_template(
        "add_undergraduate.html",
        title="Add Undergraduate Record"
    )
# ---------------------------------------------------------
# UNDERGRADUATE - UPDATE
# ---------------------------------------------------------
@app.route("/update-undergraduate/<int:id>", methods=["GET", "POST"])
def update_undergraduate(id):
    conn = get_db_connection()
    row = conn.execute(
        "SELECT * FROM Undergraduate WHERE Student_ID = ?",
        (id,)
    ).fetchone()

    if not row:
        flash("Record not found!", "danger")
        return redirect(url_for("undergraduate"))

    if request.method == "POST":
        student_id = request.form["student_id"]
        year_level = request.form["year_level"]
        grad_year = request.form["expected_grad_year"]

        conn.execute("""
            UPDATE Undergraduate
            SET Student_ID = ?, Year_Level = ?, Expected_Grad_Year = ?
            WHERE Student_ID = ?
        """, (student_id, year_level, grad_year, id))
        conn.commit()
        conn.close()

        flash("Undergraduate record updated!", "success")
        return redirect(url_for("undergraduate"))

    return render_template(
        "update_undergraduate.html",
        title="Update Undergraduate Record",
        record=row
    )
# ---------------------------------------------------------
# GRADUATE - LIST
# ---------------------------------------------------------
@app.route("/graduate")
def graduate():
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM Graduate").fetchall()
    conn.close()

    return render_template(
        "graduate.html",
        title="Graduate Students",
        grads=rows
    )
# ---------------------------------------------------------
# GRADUATE - ADD
# ---------------------------------------------------------
@app.route("/add-graduate", methods=["GET", "POST"])
def add_graduate():
    if request.method == "POST":
        student_id = request.form["student_id"]
        degree_type = request.form["degree_type"]
        research_area = request.form["research_area"]
        supervisor = request.form["supervisor"]

        conn = get_db_connection()
        conn.execute("""
            INSERT INTO Graduate (Student_ID, Degree_Type, Research_Area, Supervisor)
            VALUES (?, ?, ?, ?)
        """, (student_id, degree_type, research_area, supervisor))
        conn.commit()
        conn.close()

        flash("Graduate record added!", "success")
        return redirect(url_for("graduate"))

    return render_template(
        "add_graduate.html",
        title="Add Graduate Record"
    )
# ---------------------------------------------------------
# GRADUATE - UPDATE
# ---------------------------------------------------------
@app.route("/update-graduate/<int:id>", methods=["GET", "POST"])
def update_graduate(id):
    conn = get_db_connection()
    row = conn.execute(
        "SELECT * FROM Graduate WHERE Student_ID = ?",
        (id,)
    ).fetchone()

    if not row:
        flash("Record not found!", "danger")
        return redirect(url_for("graduate"))

    if request.method == "POST":
        student_id = request.form["student_id"]
        degree_type = request.form["degree_type"]
        research_area = request.form["research_area"]
        supervisor = request.form["supervisor"]

        conn.execute("""
            UPDATE Graduate
            SET Student_ID = ?, Degree_Type = ?, Research_Area = ?, Supervisor = ?
            WHERE Student_ID = ?
        """, (student_id, degree_type, research_area, supervisor, id))
        conn.commit()
        conn.close()

        flash("Graduate record updated!", "success")
        return redirect(url_for("graduate"))

    return render_template(
        "update_graduate.html",
        title="Update Graduate Record",
        record=row
    )
# ---------------------------------------------------------
# STUDENT DEGREE - LIST
# ---------------------------------------------------------
@app.route("/degrees")
def degrees():
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM Student_Degree").fetchall()
    conn.close()

    return render_template(
        "degrees.html",
        title="Student Degrees",
        degrees=rows
    )
# ---------------------------------------------------------
# STUDENT DEGREE - ADD
# ---------------------------------------------------------
@app.route("/add-degree", methods=["GET", "POST"])
def add_degree():
    if request.method == "POST":
        student_id = request.form["student_id"]
        dept_id = request.form["dept_id"]
        program_name = request.form["program_name"]
        program_type = request.form["program_type"]
        university = request.form["university"]

        conn = get_db_connection()
        conn.execute("""
            INSERT INTO Student_Degree 
            (Student_ID, Dept_ID, Program_Name, Program_Type, University)
            VALUES (?, ?, ?, ?, ?)
        """, (student_id, dept_id, program_name, program_type, university))
        conn.commit()
        conn.close()

        flash("Degree record added successfully!", "success")
        return redirect(url_for("degrees"))

    return render_template(
        "add_degree.html",
        title="Add Student Degree"
    )
# ---------------------------------------------------------
# STUDENT DEGREE - UPDATE
# ---------------------------------------------------------
@app.route("/update-degree/<int:s_id>/<int:d_id>/<program>", methods=["GET", "POST"])
def update_degree(s_id, d_id, program):
    conn = get_db_connection()
    row = conn.execute("""
        SELECT * FROM Student_Degree
        WHERE Student_ID = ? AND Dept_ID = ? AND Program_Name = ?
    """, (s_id, d_id, program)).fetchone()

    if not row:
        flash("Record not found!", "danger")
        return redirect(url_for("degrees"))

    if request.method == "POST":
        new_student_id = request.form["student_id"]
        new_dept_id = request.form["dept_id"]
        new_program_name = request.form["program_name"]
        program_type = request.form["program_type"]
        university = request.form["university"]

        conn.execute("""
            UPDATE Student_Degree
            SET Student_ID = ?, Dept_ID = ?, Program_Name = ?, Program_Type = ?, University = ?
            WHERE Student_ID = ? AND Dept_ID = ? AND Program_Name = ?
        """, (
            new_student_id, new_dept_id, new_program_name, program_type, university,
            s_id, d_id, program
        ))
        conn.commit()
        conn.close()

        flash("Degree record updated successfully!", "success")
        return redirect(url_for("degrees"))

    return render_template(
        "update_degree.html",
        title="Update Student Degree",
        degree=row
    )
# ---------------------------------------------------------
# REGISTRATION - LIST
# ---------------------------------------------------------
@app.route("/registration")
def registration():
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM Registration").fetchall()
    conn.close()

    return render_template(
        "registration.html",
        title="Registration Records",
        registration=rows
    )
# ---------------------------------------------------------
# REGISTRATION - ADD
# ---------------------------------------------------------
@app.route("/add-registration", methods=["GET", "POST"])
def add_registration():
    if request.method == "POST":
        student_id = request.form["student_id"]
        dept_id = request.form["dept_id"]
        course_id = request.form["course_id"]
        section_no = request.form["section_no"]

        conn = get_db_connection()
        conn.execute("""
            INSERT INTO Registration 
            (Registration_ID, Student_ID, Dept_ID, Course_ID, Section_No)
            VALUES (
                (SELECT COALESCE(MAX(Registration_ID), 5000) + 1 FROM Registration),
                ?, ?, ?, ?
            )
        """, (student_id, dept_id, course_id, section_no))
        conn.commit()
        conn.close()

        flash("Registration added successfully!", "success")
        return redirect(url_for("registration"))

    return render_template(
        "add_registration.html",
        title="Add Registration"
    )
# ---------------------------------------------------------
# REGISTRATION - UPDATE
# ---------------------------------------------------------
@app.route("/update-registration/<int:id>", methods=["GET", "POST"])
def update_registration(id):
    conn = get_db_connection()
    row = conn.execute(
        "SELECT * FROM Registration WHERE Registration_ID = ?",
        (id,)
    ).fetchone()

    if not row:
        flash("Registration not found!", "danger")
        return redirect(url_for("registration"))

    if request.method == "POST":
        student_id = request.form["student_id"]
        dept_id = request.form["dept_id"]
        course_id = request.form["course_id"]
        section_no = request.form["section_no"]

        conn.execute("""
            UPDATE Registration
            SET Student_ID = ?, Dept_ID = ?, Course_ID = ?, Section_No = ?
            WHERE Registration_ID = ?
        """, (student_id, dept_id, course_id, section_no, id))
        conn.commit()
        conn.close()

        flash("Registration updated successfully!", "success")
        return redirect(url_for("registration"))

    return render_template(
        "update_registration.html",
        title="Update Registration",
        registration=row
    )
# ---------------------------------------------------------
# TUITION - LIST
# ---------------------------------------------------------
@app.route("/tuition")
def tuition():
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM Tuition").fetchall()
    conn.close()

    return render_template(
        "tuition.html",
        title="Tuition Records",
        tuition=rows
    )
# ---------------------------------------------------------
# TUITION - ADD
# ---------------------------------------------------------
@app.route("/add-tuition", methods=["GET", "POST"])
def add_tuition():
    if request.method == "POST":
        student_id = request.form["student_id"]
        dept_id = request.form["dept_id"]
        payment_deadline = request.form["payment_deadline"]
        payment_amount = request.form["payment_amount"]
        payment_status = request.form["payment_status"]  # Dropdown

        conn = get_db_connection()
        conn.execute("""
            INSERT INTO Tuition 
            (Student_ID, Dept_ID, Payment_Deadline, Payment_Amount, Payment_Status)
            VALUES (?, ?, ?, ?, ?)
        """, (student_id, dept_id, payment_deadline, payment_amount, payment_status))
        conn.commit()
        conn.close()

        flash("Tuition record added successfully!", "success")
        return redirect(url_for("tuition"))

    return render_template(
        "add_tuition.html",
        title="Add Tuition Record"
    )
# ---------------------------------------------------------
# TUITION - UPDATE
# ---------------------------------------------------------
@app.route("/update-tuition/<int:s_id>/<int:d_id>", methods=["GET", "POST"])
def update_tuition(s_id, d_id):
    conn = get_db_connection()
    row = conn.execute("""
        SELECT * FROM Tuition 
        WHERE Student_ID = ? AND Dept_ID = ?
    """, (s_id, d_id)).fetchone()

    if not row:
        flash("Tuition record not found!", "danger")
        return redirect(url_for("tuition"))

    if request.method == "POST":
        new_student_id = request.form["student_id"]
        new_dept_id = request.form["dept_id"]
        payment_deadline = request.form["payment_deadline"]
        payment_amount = request.form["payment_amount"]
        payment_status = request.form["payment_status"]  # Dropdown

        conn.execute("""
            UPDATE Tuition
            SET Student_ID = ?, Dept_ID = ?, Payment_Deadline = ?, 
                Payment_Amount = ?, Payment_Status = ?
            WHERE Student_ID = ? AND Dept_ID = ?
        """, (
            new_student_id, new_dept_id, payment_deadline,
            payment_amount, payment_status,
            s_id, d_id
        ))
        conn.commit()
        conn.close()

        flash("Tuition record updated successfully!", "success")
        return redirect(url_for("tuition"))

    return render_template(
        "update_tuition.html",
        title="Update Tuition Record",
        t=row
    )
# ---------------------------------------------------------
# RUN APP
# ---------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
