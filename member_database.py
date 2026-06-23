import sqlite3

DB_NAME = "library.db"
def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def initialize_database():
    with get_connection() as conn:
        cursor = conn.cursor()

        # Member Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Members (
            member_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            created_at TEXT NOT NULL
        );
        """)

def add_member(first_name, last_name, email, phone, created_at):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Members (first_name, last_name, email, phone, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (first_name, last_name, email, phone, created_at))
        conn.commit()

# get
def get_member_by_id(member_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(""" SELECT * FROM Members WHERE member_id = ? """, (member_id,))
        return cursor.fetchone()
    
def get_all_members():
     with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Members")
        return cursor.fetchall()
    
# update
def update_member(first_name, last_name, email, phone, created_at, member_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE Members SET first_name = ?, last_name = ?, phone = ? WHERE member_id = ?",(first_name, last_name, email, phone, created_at, member_id,))
        conn.commit()

# delete
def delete_member(member_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute( " DELETE FROM Members WHERE member_id = ?", (member_id,))
        conn.commit()    