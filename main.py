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


        self.root.mainloop()

    # Options menus appear when the navigation buttons are selected
    def book_options(self):
            option_frame = tk.Frame(self.root, width = 700, height = 100)
            option_frame.grid(row = 1, column=0)
            tk.Button(option_frame, text = "Add Book").grid(row = 1, column= 0)

    def member_options(self):
            option_frame = tk.Frame(self.root, width = 700, height = 100)
            option_frame.grid(row = 1, column=0)
            tk.Button(option_frame, text = "Add Member", command = self.add_member).grid(row = 1, column= 0)
            tk.Button(option_frame, text = "Update Member").grid(row = 1, column= 1)
            tk.Button(option_frame, text = "Delete Member").grid(row = 1, column= 2)

    def report_options(self):
            option_frame = tk.Frame(self.root, width = 700, height = 100)
            option_frame.grid(row = 1, column=0)
            tk.Button(option_frame, text = "View All Checked Out Books").grid(row = 1, column= 0)
            tk.Button(option_frame, text = "View Overdue Books").grid(row = 1, column= 1)
            tk.Button(option_frame, text = "View All Library Members", command = self.report_all_members).grid(row = 1, column= 2)

    # Interacting with the database
    def add_member(self):
          # ADDING TEST DATA. REPLACE WITH REAL ADD FORM AND FUNCTION LATER
          self.member.Member.add_member(self.member, "Jane", "Doe", "Test", "123-456-7890", "2026-06-23")
          print("Test Member Added")

    def report_all_members(self):
          all_members = self.member.Member.get_all_members(self.member)
          for member in all_members:
                print(member[1])
                print(member[2])

def main():
    LibraryProgram()

main()
