import tkinter as tk
import Member

class LibraryProgram:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Library Inventory")
        self.root.geometry("700x500")
        
        self.member = Member

        #navigation bar
        nav_frame = tk.Frame(self.root, width = 700, height = 100)
        nav_frame.grid(row = 0, column= 0)

        tk.Button(nav_frame, text = "Books", bg = "lightgrey", padx= 30, command= self.book_options).grid(row = 0, column = 0, padx = 10)
        tk.Button(nav_frame, text = "Members", bg = "lightgrey", padx= 30, command= self.member_options).grid(row = 0, column = 1, padx = 10)
        tk.Button(nav_frame, text = "Checkouts", bg = "lightgrey", padx= 30).grid(row = 0, column = 2, padx = 10)
        tk.Button(nav_frame, text = "Reports", bg = "lightgrey", padx= 30, command= self.report_options).grid(row = 0, column = 3, padx = 10)

        self.option_frame = tk.Frame(self.root, width = 700, height = 100)
        self.option_frame.grid(row = 1, column=0)

        self.root.mainloop()

    # Options menus appear when the navigation buttons are selected
    def book_options(self):
            # remove any previous menu
            for object in self.option_frame.grid_slaves():
                 object.grid_forget()
            tk.Button(self.option_frame, text = "Add Book").grid(row = 1, column= 0)
            tk.Button(self.option_frame, text = "Update Book").grid(row = 1, column= 1)
            tk.Button(self.option_frame, text = "Delete Book").grid(row = 1, column= 2)

    def member_options(self):
            # remove any previous menu
            for object in self.option_frame.grid_slaves():
                 object.grid_forget()
            tk.Button(self.option_frame, text = "Add Member", command = self.add_member).grid(row = 1, column= 0, padx = 10)
            tk.Button(self.option_frame, text = "Update Member").grid(row = 1, column= 1, padx = 10)
            tk.Button(self.option_frame, text = "Delete Member", command = self.delete_member_menu).grid(row = 1, column= 2, padx = 10)

    def report_options(self):
            
            # remove any previous menu
            for object in self.option_frame.grid_slaves():
                 object.grid_forget()
            tk.Button(self.option_frame, text = "View All Checked Out Books").grid(row = 1, column= 0, padx = 10)
            tk.Button(self.option_frame, text = "View Overdue Books").grid(row = 1, column= 1, padx = 10)
            tk.Button(self.option_frame, text = "View All Library Members", command = self.report_all_members).grid(row = 1, column= 2, padx = 10)

    # Menus
    def delete_member_menu(self):

        def delete_member_button():
            id = self.id_entry.get()
            try:
                id = int(id)
                self.member.Member.delete_member(self.member, id)
                print("Member deleted")
            except:
                print("invalid ID")

        menu_frame = tk.Frame(self.root, width = 700, height = 100)
        menu_frame.grid(row = 2, column = 0)
    
        tk.Label(menu_frame, text = "Enter ID").grid(row = 1, column= 0, padx = 10)
        self.id_entry = tk.Entry(menu_frame)
        self.id_entry.grid(row = 1, column= 1, padx = 10)
        delete_button = tk.Button(menu_frame, text = "Delete", command = delete_member_button)
        delete_button.grid(row = 2, column = 1, padx = 10)

        
        

    # Interacting with the database
    def add_member(self):
          # ADDING TEST DATA. REPLACE WITH REAL ADD FORM AND FUNCTION LATER
          self.member.Member.add_member(self.member, "Jane", "Doe", "Test", "123-456-7890", "2026-06-23")
          print("Test Member Added")

    

    def report_all_members(self):
          all_members = self.member.Member.get_all_members(self.member)
          report_frame = tk.Frame(self.root, width = 700, height = 500)
          report_frame.grid(row = 3, column = 0)
        
          tk.Label(report_frame, text = "ID").grid(row = 0, column = 0, padx=30)
          tk.Label(report_frame, text = "First Name").grid(row = 0, column = 1, padx=30)
          tk.Label(report_frame, text = "Last Name").grid(row = 0, column = 2, padx=30)
          tk.Label(report_frame, text = "Email").grid(row = 0, column = 3, padx=30)
          tk.Label(report_frame, text = "Phone").grid(row = 0, column = 4, padx=30)  

          count = 1
          for member in all_members:
                tk.Label(report_frame, text = member[0]).grid(row = count, column = 0, padx=30)
                tk.Label(report_frame, text = member[1]).grid(row = count, column = 1, padx=30)
                tk.Label(report_frame, text = member[2]).grid(row = count, column = 2, padx=30)
                tk.Label(report_frame, text = member[3]).grid(row = count, column = 3, padx=30)
                tk.Label(report_frame, text = member[4]).grid(row = count, column = 4, padx=30)
                count += 1


def main():
    LibraryProgram()

main()
