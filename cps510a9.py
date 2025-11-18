import sqlite3

# Function to connect to the local SQLite database
def connect_db():
    return sqlite3.connect('university.db')

# Function to drop all tables (handles dependencies by dropping in reverse creation order)
def drop_tables(conn):
    cursor = conn.cursor()
    tables = [
        'Tuition', 'Registration', 'Student_Degree', 'Graduate', 'Undergraduate',
        'Student_Major', 'Student', 'Instructor_Courses_Taught', 'Section',
        'Course', 'Instructor', 'Department', 'System_Admin'
    ]
    for table in tables:
        cursor.execute(f"DROP TABLE IF EXISTS {table}")
    conn.commit()
    print("All tables have been dropped successfully.")

# Function to create all tables based on the normalized schema 
def create_tables(conn):
    cursor = conn.cursor()
    
    # System_Admin table (Admin details for system management)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS System_Admin (
            Admin_ID INTEGER PRIMARY KEY,
            Admin_Email TEXT NOT NULL,
            Admin_Username TEXT NOT NULL,
            Admin_Password TEXT NOT NULL
        )
    ''')
    
    # Department table (University departments)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Department (
            Department_ID INTEGER PRIMARY KEY,
            Department_Name TEXT NOT NULL,
            Department_Email TEXT,
            Department_Office TEXT
        )
    ''')
    
    # Instructor table (Faculty members)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Instructor (
            Instructor_ID INTEGER PRIMARY KEY,
            Instructor_Name TEXT NOT NULL,
            Instructor_Email TEXT
        )
    ''')
    
    # Course table (Courses offered by departments)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Course (
            Department_ID INTEGER,
            Course_ID INTEGER,
            Course_Name TEXT NOT NULL,
            Credits INTEGER,
            PRIMARY KEY (Department_ID, Course_ID),
            FOREIGN KEY (Department_ID) REFERENCES Department(Department_ID)
        )
    ''')
    
    # Section table (Specific sections of courses, linked to instructors)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Section (
            Department_ID INTEGER,
            Course_ID INTEGER,
            Section_NO INTEGER,
            Instructor_ID INTEGER,
            PRIMARY KEY (Department_ID, Course_ID, Section_NO),
            FOREIGN KEY (Department_ID, Course_ID) REFERENCES Course(Department_ID, Course_ID),
            FOREIGN KEY (Instructor_ID) REFERENCES Instructor(Instructor_ID)
        )
    ''')
    
    # Instructor_Courses_Taught table (Many-to-many relationship for instructors and courses)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Instructor_Courses_Taught (
            Instructor_ID INTEGER,
            Department_ID INTEGER,
            Course_ID INTEGER,
            PRIMARY KEY (Instructor_ID, Department_ID, Course_ID),
            FOREIGN KEY (Instructor_ID) REFERENCES Instructor(Instructor_ID),
            FOREIGN KEY (Department_ID, Course_ID) REFERENCES Course(Department_ID, Course_ID)
        )
    ''')
    
    # Student table (General student information)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Student (
            Student_ID INTEGER PRIMARY KEY,
            First_Name TEXT NOT NULL,
            Last_Name TEXT NOT NULL,
            Student_Email TEXT,
            Date_Of_Birth DATE,
            Phone_Number TEXT
        )
    ''')
    
    # Student_Major table (Students' majors, many-to-many)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Student_Major (
            Student_ID INTEGER,
            Major_Name TEXT,
            PRIMARY KEY (Student_ID, Major_Name),
            FOREIGN KEY (Student_ID) REFERENCES Student(Student_ID)
        )
    ''')
    
    # Undergraduate table (Specific to undergrad students)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Undergraduate (
            Student_ID INTEGER PRIMARY KEY,
            Year_Level INTEGER,
            Expected_Graduation DATE,
            FOREIGN KEY (Student_ID) REFERENCES Student(Student_ID)
        )
    ''')
    
    # Graduate table (Specific to grad students)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Graduate (
            Student_ID INTEGER PRIMARY KEY,
            Program_Level TEXT,
            Thesis_Title TEXT,
            Area_Of_Research TEXT,
            FOREIGN KEY (Student_ID) REFERENCES Student(Student_ID)
        )
    ''')
    
    # Student_Degree table (Degrees earned by students)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Student_Degree (
            Student_ID INTEGER,
            Degree_ID INTEGER,
            Degree_Name TEXT,
            Degree_Type TEXT,
            Institution_Name TEXT,
            PRIMARY KEY (Student_ID, Degree_ID),
            FOREIGN KEY (Student_ID) REFERENCES Student(Student_ID)
        )
    ''')
    
    # Registration table (Student course registrations)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Registration (
            Registration_ID INTEGER PRIMARY KEY,
            Student_ID INTEGER,
            Department_ID INTEGER,
            Course_ID INTEGER,
            Section_NO INTEGER,
            FOREIGN KEY (Student_ID) REFERENCES Student(Student_ID),
            FOREIGN KEY (Department_ID, Course_ID, Section_NO) REFERENCES Section(Department_ID, Course_ID, Section_NO)
        )
    ''')
    
    # Tuition table (Payment details for students)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Tuition (
            Student_ID INTEGER,
            Payment_ID INTEGER,
            Payment_Deadline DATE,
            Payment_Amount REAL,
            Payment_Status TEXT,
            PRIMARY KEY (Student_ID, Payment_ID),
            FOREIGN KEY (Student_ID) REFERENCES Student(Student_ID)
        )
    ''')
    
    conn.commit()
    print("All tables have been created successfully. The schema is in 3NF and BCNF as per the original design.")

# Function to populate tables with sample dummy data
def populate_tables(conn):
    cursor = conn.cursor()
    
    # Sample data for System_Admin
    cursor.execute("INSERT OR IGNORE INTO System_Admin VALUES (1, 'admin@uni.edu', 'admin', 'password123')")
    
    # Sample data for Department
    cursor.execute("INSERT OR IGNORE INTO Department VALUES (1, 'Computer Science', 'cs@uni.edu', 'Building A, Room 101')")
    cursor.execute("INSERT OR IGNORE INTO Department VALUES (2, 'Mathematics', 'math@uni.edu', 'Building B, Room 202')")
    
    # Sample data for Instructor
    cursor.execute("INSERT OR IGNORE INTO Instructor VALUES (1, 'Dr. Jane Smith', 'jane.smith@uni.edu')")
    cursor.execute("INSERT OR IGNORE INTO Instructor VALUES (2, 'Dr. John Doe', 'john.doe@uni.edu')")
    
    # Sample data for Course
    cursor.execute("INSERT OR IGNORE INTO Course VALUES (1, 510, 'Database Systems', 3)")
    cursor.execute("INSERT OR IGNORE INTO Course VALUES (2, 101, 'Calculus I', 4)")
    
    # Sample data for Section
    cursor.execute("INSERT OR IGNORE INTO Section VALUES (1, 510, 1, 1)")
    cursor.execute("INSERT OR IGNORE INTO Section VALUES (2, 101, 1, 2)")
    
    # Sample data for Instructor_Courses_Taught
    cursor.execute("INSERT OR IGNORE INTO Instructor_Courses_Taught VALUES (1, 1, 510)")
    cursor.execute("INSERT OR IGNORE INTO Instructor_Courses_Taught VALUES (2, 2, 101)")
    
    # Sample data for Student
    cursor.execute("INSERT OR IGNORE INTO Student VALUES (1, 'Alice', 'Johnson', 'alice@uni.edu', '2000-05-15', '555-1234')")
    cursor.execute("INSERT OR IGNORE INTO Student VALUES (2, 'Bob', 'Lee', 'bob@uni.edu', '1999-08-20', '555-5678')")
    
    # Sample data for Student_Major
    cursor.execute("INSERT OR IGNORE INTO Student_Major VALUES (1, 'Computer Science')")
    cursor.execute("INSERT OR IGNORE INTO Student_Major VALUES (2, 'Mathematics')")
    
    # Sample data for Undergraduate
    cursor.execute("INSERT OR IGNORE INTO Undergraduate VALUES (1, 4, '2024-06-01')")
    
    # Sample data for Graduate
    cursor.execute("INSERT OR IGNORE INTO Graduate VALUES (2, 'Masters', 'AI Ethics', 'Artificial Intelligence')")
    
    # Sample data for Student_Degree
    cursor.execute("INSERT OR IGNORE INTO Student_Degree VALUES (1, 1, 'BSc Computer Science', 'Bachelor', 'University X')")
    
    # Sample data for Registration
    cursor.execute("INSERT OR IGNORE INTO Registration VALUES (1, 1, 1, 510, 1)")
    cursor.execute("INSERT OR IGNORE INTO Registration VALUES (2, 2, 2, 101, 1)")
    
    # Sample data for Tuition
    cursor.execute("INSERT OR IGNORE INTO Tuition VALUES (1, 1, '2024-01-15', 1500.00, 'Paid')")
    cursor.execute("INSERT OR IGNORE INTO Tuition VALUES (2, 1, '2024-01-15', 2000.00, 'Pending')")
    
    conn.commit()
    print("Tables populated with sample dummy data.")

# Function for querying tables (supports read, update, delete, search based on user input)
def query_tables(conn):
    while True:
        print("\nQuery Sub-Menu:")
        print("1. Read all records from a table")
        print("2. Update a record")
        print("3. Delete a record")
        print("4. Search for specific records")
        print("5. Return to main menu")
        sub_choice = input("Enter your choice: ")
        
        if sub_choice == '1':
            table = input("Enter table name to read: ")
            cursor = conn.cursor()
            try:
                cursor.execute(f"SELECT * FROM {table}")
                rows = cursor.fetchall()
                if rows:
                    print(f"Records in {table}:")
                    for row in rows:
                        print(row)
                else:
                    print("No records found.")
            except sqlite3.Error as e:
                print(f"Error reading table: {e}")
        
        elif sub_choice == '2':
            table = input("Enter table name to update: ")
            set_clause = input("Enter SET clause (e.g., 'First_Name = \"NewName\"'): ")
            where_clause = input("Enter WHERE clause (e.g., 'Student_ID = 1'): ")
            cursor = conn.cursor()
            try:
                cursor.execute(f"UPDATE {table} SET {set_clause} WHERE {where_clause}")
                conn.commit()
                print(f"Updated {cursor.rowcount} record(s).")
            except sqlite3.Error as e:
                print(f"Error updating record: {e}")
        
        elif sub_choice == '3':
            table = input("Enter table name to delete from: ")
            where_clause = input("Enter WHERE clause (e.g., 'Student_ID = 1'): ")
            cursor = conn.cursor()
            try:
                cursor.execute(f"DELETE FROM {table} WHERE {where_clause}")
                conn.commit()
                print(f"Deleted {cursor.rowcount} record(s).")
            except sqlite3.Error as e:
                print(f"Error deleting record: {e}")
        
        elif sub_choice == '4':
            table = input("Enter table name to search: ")
            where_clause = input("Enter WHERE clause (e.g., 'First_Name LIKE \"%Alice%\"'): ")
            cursor = conn.cursor()
            try:
                cursor.execute(f"SELECT * FROM {table} WHERE {where_clause}")
                rows = cursor.fetchall()
                if rows:
                    print("Search results:")
                    for row in rows:
                        print(row)
                else:
                    print("No matching records found.")
            except sqlite3.Error as e:
                print(f"Error searching: {e}")
        
        elif sub_choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

# Main function with command-line menu loop
def main():
    conn = connect_db()
    print("Connected to local database (university.db).")
    
    while True:
        print("\nMain Menu:")
        print("1. Drop Tables")
        print("2. Create Tables")
        print("3. Populate Tables")
        print("4. Query Tables (Read/Update/Delete/Search)")
        print("5. Exit")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            drop_tables(conn)
        elif choice == '2':
            create_tables(conn)
        elif choice == '3':
            populate_tables(conn)
        elif choice == '4':
            query_tables(conn)
        elif choice == '5':
            print("Exiting application.")
            break
        else:
            print("Invalid choice. Please try again.")
    
    conn.close()

if __name__ == "__main__":
    main()