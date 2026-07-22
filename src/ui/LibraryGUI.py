import tkinter as tk

from src.services.BookService import BookService
from src.services.MemberService import MemberService
from src.services.CheckoutService import CheckoutService


# views are still being developed. Only the MemberView is currently functional.
from src.ui.member_view import MemberView
#from src.ui.book_view import BookView
#from src.ui.checkout_view import CheckoutView
#from src.ui.reports_view import ReportsView


class LibraryGUI:
    def __init__(self, database):
        self.root = tk.Tk()
        self.root.title("Library Inventory")
        self.root.geometry("1100x715")

        self.book_service = BookService(database)
        self.member_service = MemberService(database)
        self.checkout_service = CheckoutService(database)

        self.create_navigation()

        self.content_frame = tk.Frame(self.root)
        self.content_frame.pack(fill="both", expand=True)

        self.show_books()

        self.root.mainloop()

    def create_navigation(self):
        nav_frame = tk.Frame(self.root)
        nav_frame.pack(fill="x", padx=10, pady=10)

        # Use grid so buttons expand equally when the window is resized
        for i in range(4):
            nav_frame.columnconfigure(i, weight=1)

        tk.Button(nav_frame, text="Books", command=self.show_books).grid(
            row=0, column=0, sticky="ew", padx=5
        )

        tk.Button(nav_frame, text="Members", command=self.show_members).grid(
            row=0, column=1, sticky="ew", padx=5
        )

        tk.Button(nav_frame, text="Checkouts", command=self.show_checkouts).grid(
            row=0, column=2, sticky="ew", padx=5
        )

        tk.Button(nav_frame, text="Reports", command=self.show_reports).grid(
            row=0, column=3, sticky="ew", padx=5
        )

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_books(self):
        # BookView is still being developed, leave this view empty for now
        self.clear_content()

    def show_members(self):
        self.clear_content()

        view = MemberView(
            self.content_frame,
            self.member_service,
        )
        view.pack(fill="both", expand=True)

    def show_checkouts(self):
        # CheckoutView is still being developed, leave this view empty for now
        self.clear_content()

    def show_reports(self):
        # ReportsView is still being developed, leave this view empty for now
        self.clear_content()
