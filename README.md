🎓 University Enrollment System 

A full University Enrollment Management System built using Flask + SQLite, supporting 12 complete modules with full CRUD functionality.

🔗 Live Repository

GitHub:
https://github.com/ArafAjwad/CPS530-A9-University-System

📌 Features Overview

The system includes 12 interactive modules, grouped into three categories:

🧑‍🎓 Student Services

Students

Majors

Undergraduate Records

Graduate Records

Degrees

🏫 Academic Records

Departments

Courses

Sections

Instructors

Instructor Courses Taught

🗂 Administration

Registration

Tuition

Each module supports:
✔ Create
✔ Read
✔ Update
✔ Delete
✔ Auto-generated IDs
✔ Flash validation messages
✔ Clean, responsive forms

🖥️ How to Launch the Project
1️⃣ Download the Project

Clone the repository:

git clone https://github.com/ArafAjwad/CPS530-A9-University-System.git


or download the ZIP and extract it.

2️⃣ Install Dependencies

Make sure Python 3.x is installed.

Install Flask:

pip install flask

3️⃣ Run the Application

Navigate into the project folder and run:

python app.py

4️⃣ Open in Browser

Visit:

http://127.0.0.1:5000/


Your app is now running.

🗄️ Database Information

This project uses SQLite via:

university.db


✔ Fully embedded
✔ Auto-loaded
✔ No configuration required
✔ No Oracle or external DB needed

If you delete the DB, you can rebuild it using:

initialize_db.py

🧭 How to Use the System
🏠 Homepage Dashboard

The landing page contains:

Animated statistics

12 clickable tiles

Light/Dark mode toggle

Smooth UI layout

🔧 CRUD Operations

Every module includes:

Add new record

Edit existing record

🧩 Modular Structure

All HTML pages are inside:

/templates


Flask views are inside:

app.py

📦 File Structure
CPS530-A9-University-System/
│
├── app.py                 # Main Flask Application
├── initialize_db.py       # Optional database initializer
├── schema.sql             # Database schema
├── university.db          # SQLite database (pre-populated)
│
├── templates/             # All HTML UI files
│   ├── index.html
│   ├── students.html
│   ├── add_student.html
│   ├── update_student.html
│   ├── departments.html
│   ├── ...
│
└── a9.pdf                 # User guide (included in submission)

📘 Deliverables (For CPS530 Submission)

The repository includes:

✔ GitHub Repository Link
✔ ZIP File (a9.zip)
✔ PDF User Guide (a9.pdf)

Launch instructions

Features

Screenshots

Usage guide


--- Developed by Araf Ajwad
