import MemberService
import LibraryDatabase

class Member:
    def __init__(self, member_id, first_name, last_name, email, phone):
        self.member_id = member_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone


    #update
    def update_member(self, first_name, last_name, email, phone, created_at, member_id):
        LibraryDatabase.executeUpdate("UPDATE Members SET first_name = ?, last_name = ?, phone = ? WHERE member_id = ?",(first_name, last_name, email, phone, created_at, member_id,))


    #get all
    def get_all_members(self):
        return LibraryDatabase.executeQuery("SELECT * FROM Members", None)
    

    