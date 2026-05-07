import sqlite3

conn = sqlite3.connect("daycare.db")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS attendance")
cur.execute("DROP TABLE IF EXISTS children")
cur.execute("DROP TABLE IF EXISTS users")

cur.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT NOT NULL
)
""")

cur.execute("""
CREATE TABLE children (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    date_of_birth TEXT,
    grade TEXT,
    age INTEGER NOT NULL,
    schedule_type TEXT,
    parent_user_id INTEGER,
    parent_name TEXT,
    parent_address TEXT,
    parent_phone TEXT,
    emergency_contact TEXT,
    immunization_status TEXT,
    FOREIGN KEY (parent_user_id) REFERENCES users(id)
)
""")

cur.execute("""
CREATE TABLE attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    child_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    status TEXT NOT NULL,
    check_in_time TEXT,
    check_out_time TEXT,
    FOREIGN KEY (child_id) REFERENCES children(id)
)
""")

cur.execute(
    "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
    ("admin1", "admin123", "admin")
)
cur.execute(
    "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
    ("teacher1", "teach123", "teacher")
)
cur.execute(
    "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
    ("parent1", "parent123", "parent")
)
cur.execute(
    "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
    ("parent2", "parent234", "parent")
)
cur.execute(
    "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
    ("parent3", "parent345", "parent")
)

parent1_id = cur.execute("SELECT id FROM users WHERE username = 'parent1'").fetchone()[0]
parent2_id = cur.execute("SELECT id FROM users WHERE username = 'parent2'").fetchone()[0]
parent3_id = cur.execute("SELECT id FROM users WHERE username = 'parent3'").fetchone()[0]

cur.execute("""
INSERT INTO children
(name, date_of_birth, grade, age, schedule_type, parent_user_id, parent_name, parent_address, parent_phone, emergency_contact, immunization_status)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    "Lilly", "2020-05-14", "Pre-K", 4, "Full Day", parent1_id,
    "Sarah Johnson", "12 Oak Street", "555-111-2222", "Michael Johnson - 555-111-3333", "Updated"
))

cur.execute("""
INSERT INTO children
(name, date_of_birth, grade, age, schedule_type, parent_user_id, parent_name, parent_address, parent_phone, emergency_contact, immunization_status)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    "Ethan", "2021-03-02", "Nursery", 3, "Half Day", parent2_id,
    "Daniel Smith", "44 Pine Avenue", "555-222-3333", "Rebecca Smith - 555-222-4444", "Needs Update"
))

cur.execute("""
INSERT INTO children
(name, date_of_birth, grade, age, schedule_type, parent_user_id, parent_name, parent_address, parent_phone, emergency_contact, immunization_status)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    "Maya", "2019-11-20", "Kindergarten", 5, "School Age", parent3_id,
    "Angela Brown", "78 Maple Drive", "555-333-4444", "Chris Brown - 555-333-5555", "Updated"
))

conn.commit()
conn.close()

print("Database initialized successfully.")