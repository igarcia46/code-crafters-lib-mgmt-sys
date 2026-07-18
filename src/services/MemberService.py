from src.database.database_service import DatabaseService

class MemberService:
    def __init__(self, database):
         self.database = database

    def addMember(self, first_name, last_name, phone, email):
           return DatabaseService.add_member(self.database, first_name, last_name, phone, email)
    def getMemberById(self, member_id):
        return DatabaseService.get_member_by_id(self.database, member_id)

    def updateMember(self, member_id, first_name, last_name, phone, email):
         return DatabaseService.update_member(self.database, first_name, last_name, phone, email)
    
    def removeMember(self, member_id):
        return DatabaseService.delete_member(self.database, member_id)
    
    def searchMember(self, search_term):
        return DatabaseService.search_members(self.database,search_term)
    
    def getAllMembers(self):
         return DatabaseService.get_all_members(self.database)
    
