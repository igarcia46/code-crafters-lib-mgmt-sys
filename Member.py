import member_database

class Member:
    def __init__(self, member_id, first_name, last_name, email, phone):
        self.member_id = member_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone

    #add
    def add_member (self, first_name, last_name, email, phone, created_at):
        member_database.add_member(first_name, last_name, email, phone, created_at)

    #update
    def update_member (self, first_name, last_name, email, phone, created_at, member_id):
        member_database.update_member(first_name, last_name, email, phone, created_at, member_id)

    #delete
    def delete_member (self, member_id):
        member_database.delete_member(member_id)

    #get all
    def get_all_members(self):
        return member_database.get_all_members()

    