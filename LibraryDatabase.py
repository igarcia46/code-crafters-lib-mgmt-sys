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
        
        # Book Table (PLACE HOLDER)

        # Checkout Table (PLACE HOLDER)

def executeQuery(query, values): 
     if(values == None):
          print(query)
          with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return cursor.fetchall()
     else: 
        with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, values)
                return cursor.fetchone()
     
def executeUpdate(query, values):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()
    
#def closeConnection():
     #place holder

