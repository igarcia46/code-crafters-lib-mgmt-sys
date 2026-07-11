import sqlite3
import LibraryDatabase

class MemberService:
    def add_member(self, first_name, last_name, email, phone, created_at):
            LibraryDatabase.executeUpdate("""
                INSERT INTO Members (first_name, last_name, email, phone, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (first_name, last_name, email, phone, created_at))

    # get
    def get_member_by_id(self, member_id):
        return LibraryDatabase.executeQuery(""" SELECT * FROM Members WHERE member_id = ? """, (member_id,))

    # delete
    def delete_member(self, member_id):
        LibraryDatabase.executeUpdate( " DELETE FROM Members WHERE member_id = ?", (member_id,))
