import MemberService
import LibraryDatabase

class Member:
    def __init__(self, member_id, first_name, last_name, email, phone):
        self.member_id = member_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone


    def update_member(self, first_name, last_name, email, phone):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone


    