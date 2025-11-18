import sqlite3

def build_database():
    conn = sqlite3.connect("university.db")
    cursor = conn.cursor()

    print("Rebuilding database...")

    with open("schema.sql", "r") as f:
        sql_script = f.read()

    cursor.executescript(sql_script)

    conn.commit()
    conn.close()

    print("Database successfully rebuilt with sample data! ✔")

if __name__ == "__main__":
    build_database()
