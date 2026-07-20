import tkinter as tk
from src.database.database_service import DatabaseService
from src.database.library_database import LibraryDatabase
from src.services.BookService import BookService
from src.services.MemberService import MemberService
from src.services.CheckoutService import CheckoutService

from models.Book import Book
from models.Member import Member
from models.Checkout import Checkout

## TEST FRONT END CODE. 

class LibraryGUI:
    def __init__(self, database):
        self.member_service = MemberService(database)
        self.book_service = BookService(database),
        self.checkout_service = CheckoutService(database)
        
        self.root = tk.Tk()
        self.root.title("Library Inventory")
        self.root.geometry("600x500")
        
        self.member = Member

        # main navigation bar
        nav_frame = tk.Frame(self.root, width = 600, height = 100)
        nav_frame.grid(row = 0, column= 0)

        tk.Button(nav_frame, text = "Books", bg = "lightgrey", padx = 30, command= self.book_options).grid(row = 0, column = 0, padx = 10)
        tk.Button(nav_frame, text = "Members", bg = "lightgrey",  padx = 30, command= self.member_options).grid(row = 0, column = 1, padx = 10)
        tk.Button(nav_frame, text = "Checkouts", bg = "lightgrey",  padx = 30, command = self.checkout_options).grid(row = 0, column = 2, padx = 10)
        tk.Button(nav_frame, text = "Reports", bg = "lightgrey", padx = 30, command= self.report_options).grid(row = 0, column = 3, padx = 10)

        #options menu frame
        self.option_frame = tk.Frame(self.root, width = 600, height = 100)
        self.option_frame.grid(row = 1, column=0)

        #center frame (for forms or report)
        self.center_frame = tk.Frame(self.root, width = 600, height = 500)
        self.center_frame.grid(row = 3, column = 0)

        self.root.mainloop()

    ### Options menus appear when the navigation buttons are selected
    def book_options(self):
            # remove any previous menu and the center content
            for object in self.option_frame.grid_slaves():
                 object.grid_forget()

            for object in self.center_frame.grid_slaves():
                 object.grid_forget()
            tk.Button(self.option_frame, text = "Add Book").grid(row = 1, column= 0, padx = 10)
            tk.Button(self.option_frame, text = "Update Book").grid(row = 1, column= 1, padx = 10)
            tk.Button(self.option_frame, text = "Delete Book").grid(row = 1, column= 2, padx = 10)

    def member_options(self):
            # remove any previous menu and the center content
            for object in self.option_frame.grid_slaves():
                 object.grid_forget()

            for object in self.center_frame.grid_slaves():
                 object.grid_forget()
            tk.Button(self.option_frame, text = "Add Member", command = self.add_member).grid(row = 1, column= 0, padx = 10)
            tk.Button(self.option_frame, text = "Update Member").grid(row = 1, column= 1, padx = 10)
            tk.Button(self.option_frame, text = "Delete Member", command = self.delete_member_menu).grid(row = 1, column= 2, padx = 10)

    def report_options(self):
            # remove any previous menu and the center content
            for object in self.option_frame.grid_slaves():
                 object.grid_forget()

            for object in self.center_frame.grid_slaves():
                 object.grid_forget()
            tk.Button(self.option_frame, text = "View All Checked Out Books").grid(row = 1, column= 0, padx = 10)
            tk.Button(self.option_frame, text = "View Overdue Books").grid(row = 1, column= 1, padx = 10)
            tk.Button(self.option_frame, text = "View All Library Members", command = self.report_all_members).grid(row = 1, column= 2, padx = 10)

    def checkout_options(self):
            # remove any previous menu and the center content
            for object in self.option_frame.grid_slaves():
                 object.grid_forget()

            for object in self.center_frame.grid_slaves():
                 object.grid_forget()
            ## place holder. add checkout form to center frame. 

    ### FORMS ###
    # delete member form
    def delete_member_menu(self):

        def delete_member_button():
            id = self.id_entry.get()
            try:
                id = int(id)
                self.member_service.removeMember(id)
                print("Member deleted")
            except:
                print("invalid ID")
        tk.Label(self.center_frame, text = "Enter ID").grid(row = 1, column= 0, padx = 10)
        self.id_entry = tk.Entry(self.center_frame)
        self.id_entry.grid(row = 1, column= 1, padx = 10)
        delete_button = tk.Button(self.center_frame, text = "Delete", command = delete_member_button)
        delete_button.grid(row = 2, column = 1, padx = 10)


    # add member form
    def add_member(self):
          # ADDING TEST DATA. REPLACE WITH REAL FORM AND FUNCTION LATER
          self.member_service.addMember("Jane","Doe", "123-456-7890", "test@gmail.com")
          print("Test Member Added")


    ### REPORTS 

    def report_all_members(self):
          #remove any previous center content
          for object in self.center_frame.grid_slaves():
                 object.grid_forget()

          all_members = self.member_service.getAllMembers()
          
          tk.Label(self.center_frame, text = "ID").grid(row = 0, column = 0, padx=30)
          tk.Label(self.center_frame, text = "First Name").grid(row = 0, column = 1, padx=30)
          tk.Label(self.center_frame, text = "Last Name").grid(row = 0, column = 2, padx=30)
          tk.Label(self.center_frame, text = "Email").grid(row = 0, column = 3, padx=30)
          tk.Label(self.center_frame, text = "Phone").grid(row = 0, column = 4, padx=30)  

          count = 1
          for member in all_members:
                print(member)
                tk.Label(self.center_frame, text = member["member_id"]).grid(row = count, column = 0, padx=30)
                tk.Label(self.center_frame, text = member["first_name"]).grid(row = count, column = 1, padx=30)
                tk.Label(self.center_frame, text = member["last_name"]).grid(row = count, column = 2, padx=30)
                tk.Label(self.center_frame, text = member["email"]).grid(row = count, column = 3, padx=30)
                tk.Label(self.center_frame, text = member["phone"]).grid(row = count, column = 4, padx=30)
                count += 1

