import tkinter as tk
from tkinter import font as tkfont

from src.services.BookService import BookService
from src.services.MemberService import MemberService
from src.services.CheckoutService import CheckoutService

# views are still being developed. Only MemberView and CheckoutView are currently functional.
from src.ui.book_view import BookView
from src.ui.member_view import MemberView
from src.ui.checkout_view import CheckoutView

# from src.ui.book_view import BookView
# from src.ui.reports_view import ReportsView


# ---------------------------------------------------------------------------
# Centralized style palette so every view/button stays visually consistent.
# ---------------------------------------------------------------------------
class Theme:
    SIDEBAR_BG = "#1f2937"       # slate-800
    SIDEBAR_ACTIVE = "#2563eb"   # blue-600
    SIDEBAR_HOVER = "#374151"    # slate-700
    SIDEBAR_TEXT = "#e5e7eb"     # slate-200
    CONTENT_BG = "#f3f4f6"       # slate-100
    CARD_BG = "#ffffff"
    CARD_BORDER = "#e5e7eb"
    ACCENT = "#2563eb"
    TEXT_DARK = "#111827"
    TEXT_MUTED = "#6b7280"
    FONT_FAMILY = "Segoe UI"


class LibraryGUI:
    def __init__(self, database):
        self.root = tk.Tk()
        self.root.title("Library Inventory")
        self.root.geometry("1100x715")
        self.root.configure(bg=Theme.CONTENT_BG)
        self.root.minsize(900, 600)

        # fonts
        self.font_heading = tkfont.Font(family=Theme.FONT_FAMILY, size=20, weight="bold")
        self.font_subheading = tkfont.Font(family=Theme.FONT_FAMILY, size=12)
        self.font_nav = tkfont.Font(family=Theme.FONT_FAMILY, size=12, weight="bold")
        self.font_stat_number = tkfont.Font(family=Theme.FONT_FAMILY, size=28, weight="bold")
        self.font_stat_label = tkfont.Font(family=Theme.FONT_FAMILY, size=11)

        # initialize services
        self.book_service = BookService(database)
        self.member_service = MemberService(database)
        self.checkout_service = CheckoutService(database)
        self.database = database

        # keep references to nav buttons so we can highlight the active one
        self.nav_buttons = {}
        self.active_view = None

        # layout: sidebar (left) + content area (right)
        self.sidebar = tk.Frame(self.root, bg=Theme.SIDEBAR_BG, width=200)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.content_frame = tk.Frame(self.root, bg=Theme.CONTENT_BG)
        self.content_frame.pack(side="right", fill="both", expand=True)

        self.create_sidebar()
        self.show_home()  # default landing view

        self.root.mainloop()

    # -----------------------------------------------------------------
    # Sidebar navigation
    # -----------------------------------------------------------------
    def create_sidebar(self):
        title = tk.Label(
            self.sidebar,
            text="📚 Library",
            bg=Theme.SIDEBAR_BG,
            fg="white",
            font=(Theme.FONT_FAMILY, 16, "bold"),
            pady=25,
        )
        title.pack(fill="x")

        nav_items = [
            ("Home", self.show_home),
            ("Books", self.show_books),
            ("Members", self.show_members),
            ("Checkouts", self.show_checkouts),
            ("Reports", self.show_reports),
        ]

        for name, command in nav_items:
            btn = self.make_nav_button(name, command)
            self.nav_buttons[name] = btn

    def make_nav_button(self, name, command):
        btn = tk.Label(
            self.sidebar,
            text=f"  {name}",
            anchor="w",
            bg=Theme.SIDEBAR_BG,
            fg=Theme.SIDEBAR_TEXT,
            font=self.font_nav,
            pady=14,
            padx=20,
            cursor="hand2",
        )
        btn.pack(fill="x")

        def on_enter(_):
            if self.active_view != name:
                btn.configure(bg=Theme.SIDEBAR_HOVER)

        def on_leave(_):
            if self.active_view != name:
                btn.configure(bg=Theme.SIDEBAR_BG)

        def on_click(_):
            command()

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        btn.bind("<Button-1>", on_click)
        return btn

    def set_active_nav(self, name):
        self.active_view = name
        for btn_name, btn in self.nav_buttons.items():
            if btn_name == name:
                btn.configure(bg=Theme.SIDEBAR_ACTIVE, fg="white")
            else:
                btn.configure(bg=Theme.SIDEBAR_BG, fg=Theme.SIDEBAR_TEXT)

    # -----------------------------------------------------------------
    # Content helpers
    # -----------------------------------------------------------------
    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def page_header(self, title_text, subtitle_text=""):
        header = tk.Frame(self.content_frame, bg=Theme.CONTENT_BG)
        header.pack(fill="x", padx=30, pady=(25, 10))

        tk.Label(
            header,
            text=title_text,
            bg=Theme.CONTENT_BG,
            fg=Theme.TEXT_DARK,
            font=self.font_heading,
        ).pack(anchor="w")

        if subtitle_text:
            tk.Label(
                header,
                text=subtitle_text,
                bg=Theme.CONTENT_BG,
                fg=Theme.TEXT_MUTED,
                font=self.font_subheading,
            ).pack(anchor="w", pady=(2, 0))

    # -----------------------------------------------------------------
    # Safe data fetch helpers (won't crash if a service method
    # isn't implemented yet in your services)
    # -----------------------------------------------------------------
    def safe_count(self, func):
        try:
            result = func()
            return len(result) if result is not None else 0
        except Exception:
            return "--"

    # -----------------------------------------------------------------
    # HOME VIEW
    # -----------------------------------------------------------------
    def show_home(self):
        self.clear_content()
        self.set_active_nav("Home")

        self.page_header("Dashboard", "Overview of your library system")

        stats_frame = tk.Frame(self.content_frame, bg=Theme.CONTENT_BG)
        stats_frame.pack(fill="x", padx=30, pady=10)

        total_books = self.safe_count(self.database.get_all_books)
        total_members = self.safe_count(
            getattr(self.member_service, "getAllMembers", lambda: None)
        )
        total_checkouts = self.safe_count(
            getattr(self.checkout_service, "getCheckoutHistory", lambda: None)
        )

        stats = [
            ("Total Books", total_books, "#2563eb"),
            ("Total Members", total_members, "#16a34a"),
            ("Active Checkouts", total_checkouts, "#d97706"),
        ]

        for i, (label, value, color) in enumerate(stats):
            self.make_stat_card(stats_frame, label, value, color, column=i)
            stats_frame.columnconfigure(i, weight=1)

        # quick-action shortcuts
        actions_frame = tk.Frame(self.content_frame, bg=Theme.CONTENT_BG)
        actions_frame.pack(fill="x", padx=30, pady=(30, 10))

        tk.Label(
            actions_frame,
            text="Quick Actions",
            bg=Theme.CONTENT_BG,
            fg=Theme.TEXT_DARK,
            font=(Theme.FONT_FAMILY, 14, "bold"),
        ).pack(anchor="w", pady=(0, 10))

        quick_row = tk.Frame(actions_frame, bg=Theme.CONTENT_BG)
        quick_row.pack(fill="x")

        self.make_action_button(quick_row, "View Books", self.show_books).pack(
            side="left", padx=(0, 10)
        )
        self.make_action_button(quick_row, "View Members", self.show_members).pack(
            side="left", padx=(0, 10)
        )
        self.make_action_button(quick_row, "View Checkouts", self.show_checkouts).pack(
            side="left", padx=(0, 10)
        )

    def make_stat_card(self, parent, label, value, color, column):
        card = tk.Frame(
            parent, bg=Theme.CARD_BG, highlightbackground=Theme.CARD_BORDER,
            highlightthickness=1, bd=0,
        )
        card.grid(row=0, column=column, sticky="nsew", padx=8, ipady=15)

        accent = tk.Frame(card, bg=color, height=4)
        accent.pack(fill="x")

        tk.Label(
            card, text=str(value), bg=Theme.CARD_BG, fg=Theme.TEXT_DARK,
            font=self.font_stat_number,
        ).pack(pady=(15, 0), padx=20, anchor="w")

        tk.Label(
            card, text=label, bg=Theme.CARD_BG, fg=Theme.TEXT_MUTED,
            font=self.font_stat_label,
        ).pack(pady=(0, 10), padx=20, anchor="w")

    def make_action_button(self, parent, text, command):
        btn = tk.Label(
            parent,
            text=text,
            bg=Theme.ACCENT,
            fg="white",
            font=self.font_nav,
            padx=18,
            pady=10,
            cursor="hand2",
        )

        def on_enter(_):
            btn.configure(bg="#1d4ed8")

        def on_leave(_):
            btn.configure(bg=Theme.ACCENT)

        def on_click(_):
            command()

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        btn.bind("<Button-1>", on_click)
        return btn

    # -----------------------------------------------------------------
    # OTHER VIEWS
    # -----------------------------------------------------------------
    def show_books(self):
        self.clear_content()
        self.set_active_nav("Books")
        self.page_header("Books", "Manage your book catalog")
        view = BookView(
        self.content_frame,
        self.book_service,
    )
        view.pack(fill="both", expand=True, padx=30, pady=(0, 20))
        tk.Label(
            self.content_frame,
            text="Book management view coming soon.",
            bg=Theme.CONTENT_BG,
            fg=Theme.TEXT_MUTED,
            font=self.font_subheading,
        ).pack(padx=30, pady=20, anchor="w")

    def show_members(self):
        self.clear_content()
        self.set_active_nav("Members")
        self.page_header("Members", "Manage library members")

        view = MemberView(
            self.content_frame,
            self.member_service,
        )
        view.pack(fill="both", expand=True, padx=30, pady=(0, 20))

    def show_checkouts(self):
        self.clear_content()
        self.set_active_nav("Checkouts")
        self.page_header("Checkouts", "Track borrowed and returned books")

        view = CheckoutView(
            self.content_frame,
            self.checkout_service,
            self.book_service,
            self.member_service,
        )
        view.pack(fill="both", expand=True, padx=30, pady=(0, 20))

    def show_reports(self):
        self.clear_content()
        self.set_active_nav("Reports")
        self.page_header("Reports", "Library statistics and insights")
        tk.Label(
            self.content_frame,
            text="Reports view coming soon.",
            bg=Theme.CONTENT_BG,
            fg=Theme.TEXT_MUTED,
            font=self.font_subheading,
        ).pack(padx=30, pady=20, anchor="w")