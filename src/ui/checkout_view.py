import tkinter as tk
from tkinter import messagebox


class Theme:
    CONTENT_BG = "#f3f4f6"
    CARD_BG = "#ffffff"
    CARD_BORDER = "#e5e7eb"
    ACCENT = "#2563eb"
    ACCENT_HOVER = "#1d4ed8"
    DANGER = "#dc2626"
    DANGER_HOVER = "#b91c1c"
    TEXT_MUTED_BG = "#e5e7eb"
    TEXT_DARK = "#111827"
    TEXT_MUTED = "#6b7280"
    FONT_FAMILY = "Segoe UI"


class CheckoutView(tk.Frame):
    def __init__(self, parent, checkout_service, book_service=None, member_service=None):
        super().__init__(parent, bg=Theme.CONTENT_BG)

        self.checkout_service = checkout_service
        self.book_service = book_service
        self.member_service = member_service

        self.build_form()
        self.build_list_section()
        self.refresh_list()

    # -----------------------------------------------------------------
    # Add-checkout form
    # -----------------------------------------------------------------
    def build_form(self):
        form_card = tk.Frame(
            self, bg=Theme.CARD_BG, highlightbackground=Theme.CARD_BORDER,
            highlightthickness=1,
        )
        form_card.pack(fill="x", pady=(0, 20))

        tk.Label(
            form_card, text="New Checkout", bg=Theme.CARD_BG, fg=Theme.TEXT_DARK,
            font=(Theme.FONT_FAMILY, 13, "bold"),
        ).grid(row=0, column=0, columnspan=4, sticky="w", padx=15, pady=(12, 8))

        tk.Label(form_card, text="Book ID", bg=Theme.CARD_BG, fg=Theme.TEXT_MUTED).grid(
            row=1, column=0, sticky="w", padx=15
        )
        self.book_id_entry = tk.Entry(form_card, width=15)
        self.book_id_entry.grid(row=2, column=0, padx=15, pady=(0, 12))

        tk.Label(form_card, text="Member ID", bg=Theme.CARD_BG, fg=Theme.TEXT_MUTED).grid(
            row=1, column=1, sticky="w"
        )
        self.member_id_entry = tk.Entry(form_card, width=15)
        self.member_id_entry.grid(row=2, column=1, padx=15, pady=(0, 12))

        checkout_btn = tk.Label(
            form_card, text="Check Out Book", bg=Theme.ACCENT, fg="white",
            font=(Theme.FONT_FAMILY, 11, "bold"), padx=16, pady=8, cursor="hand2",
        )
        checkout_btn.grid(row=2, column=2, padx=15)
        checkout_btn.bind("<Enter>", lambda e: checkout_btn.configure(bg=Theme.ACCENT_HOVER))
        checkout_btn.bind("<Leave>", lambda e: checkout_btn.configure(bg=Theme.ACCENT))
        checkout_btn.bind("<Button-1>", lambda e: self.handle_checkout())

        self.error_label = tk.Label(
            form_card, text="", bg=Theme.CARD_BG, fg=Theme.DANGER,
            font=(Theme.FONT_FAMILY, 10),
        )
        self.error_label.grid(row=3, column=0, columnspan=3, sticky="w", padx=15, pady=(0, 10))

    # -----------------------------------------------------------------
    # List of active / past checkouts
    # -----------------------------------------------------------------
    def build_list_section(self):
        tk.Label(
            self, text="Checkout History", bg=Theme.CONTENT_BG, fg=Theme.TEXT_DARK,
            font=(Theme.FONT_FAMILY, 14, "bold"),
        ).pack(anchor="w", pady=(0, 10))

        canvas = tk.Canvas(self, bg=Theme.CONTENT_BG, highlightthickness=0)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.list_frame = tk.Frame(canvas, bg=Theme.CONTENT_BG)

        self.list_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=self.list_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def refresh_list(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        try:
            history = self.checkout_service.getCheckoutHistory()
        except Exception as e:
            tk.Label(
                self.list_frame, text=f"Could not load checkouts: {e}",
                bg=Theme.CONTENT_BG, fg=Theme.DANGER,
            ).pack(anchor="w", pady=10)
            return

        if not history:
            tk.Label(
                self.list_frame, text="No checkouts yet.", bg=Theme.CONTENT_BG,
                fg=Theme.TEXT_MUTED,
            ).pack(anchor="w", pady=10)
            return

        for record in history:
            self.make_checkout_row(record)

    def make_checkout_row(self, record):
        # Matches DatabaseService.get_checkout_history() columns exactly:
        # checkout_id, book_title, member_name, checkout_date, due_date, return_date
        checkout_id = record["checkout_id"]
        book_title = record["book_title"]
        member_name = record["member_name"]
        due_date = record["due_date"]
        return_date = record["return_date"]

        status = "RETURNED" if return_date else "CHECKED OUT"

        row = tk.Frame(
            self.list_frame, bg=Theme.CARD_BG, highlightbackground=Theme.CARD_BORDER,
            highlightthickness=1,
        )
        row.pack(fill="x", pady=5)

        detail_text = f'"{book_title}"  →  {member_name}   |   Due: {due_date}'
        if return_date:
            detail_text += f"   |   Returned: {return_date}"

        info = tk.Label(
            row,
            text=detail_text,
            bg=Theme.CARD_BG, fg=Theme.TEXT_DARK, font=(Theme.FONT_FAMILY, 11),
            padx=15, pady=10,
        )
        info.pack(side="left")

        status_color = Theme.TEXT_MUTED if status == "RETURNED" else Theme.ACCENT
        status_label = tk.Label(
            row, text=f"[{status}]", bg=Theme.CARD_BG, fg=status_color,
            font=(Theme.FONT_FAMILY, 10, "bold"),
        )
        status_label.pack(side="left", padx=10)

        if status != "RETURNED":
            return_btn = tk.Label(
                row, text="Return", bg=Theme.DANGER, fg="white",
                font=(Theme.FONT_FAMILY, 10, "bold"), padx=12, pady=6, cursor="hand2",
            )
            return_btn.pack(side="right", padx=10)
            return_btn.bind("<Enter>", lambda e, b=return_btn: b.configure(bg=Theme.DANGER_HOVER))
            return_btn.bind("<Leave>", lambda e, b=return_btn: b.configure(bg=Theme.DANGER))
            return_btn.bind("<Button-1>", lambda e, cid=checkout_id: self.handle_return(cid))

    # -----------------------------------------------------------------
    # Actions
    # -----------------------------------------------------------------
    def handle_checkout(self):
        self.error_label.configure(text="")
        book_id = self.book_id_entry.get().strip()
        member_id = self.member_id_entry.get().strip()

        if not book_id or not member_id:
            self.error_label.configure(text="Please enter both a Book ID and Member ID.")
            return

        try:
            self.checkout_service.checkOutBook(int(book_id), int(member_id))
            self.book_id_entry.delete(0, tk.END)
            self.member_id_entry.delete(0, tk.END)
            self.refresh_list()
        except ValueError as e:
            self.error_label.configure(text=str(e))
        except Exception as e:
            messagebox.showerror("Checkout Failed", str(e))

    def handle_return(self, checkout_id):
        try:
            self.checkout_service.returnBook(checkout_id)
            self.refresh_list()
        except Exception as e:
            messagebox.showerror("Return Failed", str(e))