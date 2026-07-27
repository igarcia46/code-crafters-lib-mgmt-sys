import tkinter as tk
from tkinter import ttk


class ReportsView(tk.Frame):
    BG = "#f3f4f6"
    CARD_BG = "#ffffff"
    BORDER = "#e5e7eb"
    ACCENT = "#2563eb"
    ACCENT_HOVER = "#1d4ed8"
    TEXT = "#111827"
    MUTED = "#6b7280"
    FONT = "Segoe UI"

    def __init__(self, parent, book_service, checkout_service):
        super().__init__(parent, bg=self.BG)
        self.book_service = book_service
        self.checkout_service = checkout_service
        self.build_view()

    def build_view(self):
        for widget in self.winfo_children():
            widget.destroy()

        books = self.book_service.getAllBooks()
        overdue = self.checkout_service.getOverdueBooks()

        available = sum(book["status"] == "AVAILABLE" for book in books)
        checked_out = sum(book["status"] == "CHECKED_OUT" for book in books)

        summary = tk.Frame(self, bg=self.BG)
        summary.pack(fill="x", pady=(0, 20))

        stats = [
            ("Total Books", len(books)),
            ("Available", available),
            ("Checked Out", checked_out),
        ]

        for column, (label, value) in enumerate(stats):
            card = tk.Frame(
                summary,
                bg=self.CARD_BG,
                highlightbackground=self.BORDER,
                highlightthickness=1,
            )
            card.grid(row=0, column=column, sticky="nsew", padx=6, ipady=12)
            summary.columnconfigure(column, weight=1)

            tk.Label(
                card,
                text=value,
                bg=self.CARD_BG,
                fg=self.TEXT,
                font=(self.FONT, 22, "bold"),
            ).pack(anchor="w", padx=15, pady=(10, 0))

            tk.Label(
                card,
                text=label,
                bg=self.CARD_BG,
                fg=self.MUTED,
                font=(self.FONT, 10),
            ).pack(anchor="w", padx=15, pady=(0, 10))

        tk.Label(
            self,
            text="Overdue Books",
            bg=self.BG,
            fg=self.TEXT,
            font=(self.FONT, 14, "bold"),
        ).pack(anchor="w", pady=(0, 8))

        columns = ("book", "member", "due_date", "email", "phone")
        table = ttk.Treeview(self, columns=columns, show="headings", height=10)

        headings = {
            "book": "Book",
            "member": "Member",
            "due_date": "Due Date",
            "email": "Email",
            "phone": "Phone",
        }

        for column, heading in headings.items():
            table.heading(column, text=heading)

        table.column("book", width=180)
        table.column("member", width=150)
        table.column("due_date", width=90)
        table.column("email", width=180)
        table.column("phone", width=110)
        table.pack(fill="both", expand=True)

        for checkout in overdue:
            table.insert(
                "",
                "end",
                values=(
                    checkout["book_title"],
                    checkout["member_name"],
                    checkout["due_date"],
                    checkout["email"],
                    checkout["phone"],
                ),
            )

        refresh_button = tk.Label(
            self,
            text="Refresh Reports",
            bg=self.ACCENT,
            fg="white",
            font=(self.FONT, 11, "bold"),
            padx=18,
            pady=10,
            cursor="hand2",
        )
        refresh_button.pack(anchor="w", pady=(15, 0))
        refresh_button.bind(
            "<Enter>",
            lambda event: refresh_button.configure(bg=self.ACCENT_HOVER),
        )
        refresh_button.bind(
            "<Leave>",
            lambda event: refresh_button.configure(bg=self.ACCENT),
        )
        refresh_button.bind("<Button-1>", lambda event: self.build_view())
