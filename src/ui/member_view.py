import tkinter as tk
from tkinter import ttk


class Theme:
    CONTENT_BG = "#f3f4f6"
    CARD_BG = "#ffffff"
    CARD_BORDER = "#e5e7eb"
    ACCENT = "#2563eb"
    ACCENT_HOVER = "#1d4ed8"
    DANGER = "#dc2626"
    DANGER_HOVER = "#b91c1c"
    SECONDARY = "#dbeafe"
    SECONDARY_FG = "#1d4ed8"
    TEXT_DARK = "#111827"
    TEXT_MUTED = "#6b7280"
    FONT_FAMILY = "Segoe UI"


class MemberView(tk.Frame):
    def __init__(self, parent, member_service):
        super().__init__(parent, bg=Theme.CONTENT_BG)

        self.member_service = member_service
        self.create_member_menu()

    def show_dialog(self, title, message, confirm=False):
        """to show a modal dialog centered over the main application window"""
        owner = self.winfo_toplevel()
        dialog = tk.Toplevel(owner)
        dialog.withdraw()
        dialog.title(title)
        dialog.resizable(False, False)
        dialog.transient(owner)
        dialog.configure(bg=Theme.CARD_BG)

        result = {"confirmed": False}

        tk.Label(
            dialog,
            text=message,
            justify="left",
            wraplength=360,
            padx=25,
            pady=20,
            bg=Theme.CARD_BG,
            fg=Theme.TEXT_DARK,
            font=(Theme.FONT_FAMILY, 11),
        ).pack()

        button_frame = tk.Frame(dialog, bg=Theme.CARD_BG)
        button_frame.pack(padx=15, pady=(0, 15))

        def close(confirmed=False):
            result["confirmed"] = confirmed
            dialog.destroy()

        if confirm:
            self._build_button(
                button_frame,
                "Yes",
                lambda: close(True),
                bg=Theme.ACCENT,
                fg="white",
                hover_bg=Theme.ACCENT_HOVER,
                width=10,
            ).pack(side="left", padx=5)
            self._build_button(
                button_frame,
                "No",
                close,
                bg=Theme.SECONDARY,
                fg=Theme.SECONDARY_FG,
                hover_bg="#bfdbfe",
                width=10,
            ).pack(side="left", padx=5)
        else:
            self._build_button(
                button_frame,
                "OK",
                close,
                bg=Theme.ACCENT,
                fg="white",
                hover_bg=Theme.ACCENT_HOVER,
                width=10,
            ).pack()

        dialog.protocol("WM_DELETE_WINDOW", close)
        dialog.update_idletasks()

        x = owner.winfo_rootx() + (owner.winfo_width() - dialog.winfo_width()) // 2
        y = owner.winfo_rooty() + (owner.winfo_height() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")

        dialog.deiconify()
        dialog.grab_set()
        dialog.focus_force()
        owner.wait_window(dialog)
        return result["confirmed"]

    def clear_view(self):
        for widget in self.winfo_children():
            widget.destroy()

    def _build_button(
        self,
        parent,
        text,
        command,
        *,
        bg,
        fg,
        hover_bg,
        hover_fg=None,
        width=None,
        side="left",
    ):
        button = tk.Button(
            parent,
            text=text,
            command=command,
            width=width,
            font=(Theme.FONT_FAMILY, 11, "bold"),
            bg=bg,
            fg=fg,
            activebackground=hover_bg,
            activeforeground=hover_fg or fg,
            cursor="hand2",
            bd=0,
            relief="flat",
            padx=14,
            pady=8,
            highlightthickness=0,
        )
        button.bind("<Enter>", lambda event, btn=button: btn.configure(bg=hover_bg))
        button.bind("<Leave>", lambda event, btn=button: btn.configure(bg=bg))
        return button

    def create_member_menu(self):
        self.clear_view()
        self.configure(bg=Theme.CONTENT_BG)

        # Minimal top spacing — keep header area clean and uncluttered
        tk.Frame(self, height=24, bg=Theme.CONTENT_BG).pack()

        button_frame = tk.Frame(self, bg=Theme.CONTENT_BG)
        button_frame.pack(pady=8)

        self._build_button(
            button_frame,
            "Add Member",
            self.show_add_member_form,
            bg=Theme.ACCENT,
            fg="white",
            hover_bg=Theme.ACCENT_HOVER,
            width=18,
        ).grid(row=0, column=0, padx=8, pady=6)

        self._build_button(
            button_frame,
            "View Members",
            self.show_all_members,
            bg=Theme.SECONDARY,
            fg=Theme.SECONDARY_FG,
            hover_bg="#bfdbfe",
            width=18,
        ).grid(row=0, column=1, padx=8, pady=6)

        self._build_button(
            button_frame,
            "Search Member",
            self.show_search_member,
            bg=Theme.SECONDARY,
            fg=Theme.SECONDARY_FG,
            hover_bg="#bfdbfe",
            width=18,
        ).grid(row=0, column=2, padx=8, pady=6)

        self._build_button(
            button_frame,
            "Delete Member",
            self.show_delete_member_form,
            bg=Theme.DANGER,
            fg="white",
            hover_bg=Theme.DANGER_HOVER,
            width=18,
        ).grid(row=0, column=3, padx=8, pady=6)

    def show_search_member(self):
        """Search members by name, phone or email and show results in a table."""
        self.clear_view()
        self.configure(bg=Theme.CONTENT_BG)

        tk.Label(
            self,
            text="Search Members",
            font=(Theme.FONT_FAMILY, 18, "bold"),
            bg=Theme.CONTENT_BG,
            fg=Theme.TEXT_DARK,
        ).pack(pady=(20, 10))

        form_frame = tk.Frame(
            self,
            bg=Theme.CARD_BG,
            highlightbackground=Theme.CARD_BORDER,
            highlightthickness=1,
            padx=20,
            pady=14,
        )
        form_frame.pack(padx=20, pady=(5, 10), fill="x")

        tk.Label(
            form_frame,
            text="Search term:",
            font=(Theme.FONT_FAMILY, 10, "bold"),
            bg=Theme.CARD_BG,
            fg=Theme.TEXT_DARK,
        ).grid(row=0, column=0, sticky="w", padx=(6, 12))

        self.search_entry = tk.Entry(form_frame, width=40)
        self.search_entry.grid(row=0, column=1, sticky="w")

        tk.Label(
            form_frame,
            text="Searches first name, last name, phone, and email.",
            font=(Theme.FONT_FAMILY, 9),
            bg=Theme.CARD_BG,
            fg=Theme.TEXT_MUTED,
        ).grid(row=1, column=0, columnspan=3, sticky="w", pady=(8, 0), padx=(6, 0))

        button_frame = tk.Frame(form_frame, bg=Theme.CARD_BG)
        button_frame.grid(row=0, column=2, padx=12)

        def do_search(event=None):
            term = self.search_entry.get().strip()
            if not term:
                self.show_dialog("Input Required", "Please enter a search term.")
                return

            try:
                results = self.member_service.searchMember(term)
            except Exception as e:
                self.show_dialog("Error", f"Search failed.\n\n{e}")
                return

            # populate results table
            for child in results_card.winfo_children():
                child.destroy()

            tree = ttk.Treeview(
                results_card, columns=("id", "first", "last", "email", "phone"), show="headings"
            )
            tree.heading("id", text="ID")
            tree.heading("first", text="First Name")
            tree.heading("last", text="Last Name")
            tree.heading("email", text="Email")
            tree.heading("phone", text="Phone")

            tree.column("id", width=70, anchor="center")
            tree.column("first", width=140, anchor="w")
            tree.column("last", width=140, anchor="w")
            tree.column("email", width=200, anchor="w")
            tree.column("phone", width=120, anchor="w")

            tree.pack(fill="both", expand=True)

            for m in results:
                tree.insert("", "end", values=(m["member_id"], m["first_name"], m["last_name"], m["email"], m["phone"]))

        self._build_button(
            button_frame,
            "Search",
            do_search,
            bg=Theme.ACCENT,
            fg="white",
            hover_bg=Theme.ACCENT_HOVER,
            width=12,
        ).pack(side="left")

        self._build_button(
            button_frame,
            "Back",
            self.create_member_menu,
            bg=Theme.SECONDARY,
            fg=Theme.SECONDARY_FG,
            hover_bg="#bfdbfe",
            width=12,
        ).pack(side="left", padx=(8, 0))

        self.search_entry.bind("<Return>", do_search)

        results_card = tk.Frame(self, bg=Theme.CARD_BG, highlightbackground=Theme.CARD_BORDER, highlightthickness=1)
        results_card.pack(fill="both", expand=True, padx=20, pady=(10, 20))

    def show_add_member_form(self):
        self.clear_view()
        self.configure(bg=Theme.CONTENT_BG)

        tk.Label(
            self,
            text="Add Member",
            font=(Theme.FONT_FAMILY, 18, "bold"),
            bg=Theme.CONTENT_BG,
            fg=Theme.TEXT_DARK,
        ).pack(pady=(20, 10))

        form_frame = tk.Frame(
            self,
            bg=Theme.CARD_BG,
            highlightbackground=Theme.CARD_BORDER,
            highlightthickness=1,
            padx=28,
            pady=24,
        )
        form_frame.pack(padx=20, pady=(5, 20))
        form_frame.columnconfigure(1, weight=1)

        tk.Label(
            form_frame,
            text="Member Details",
            font=(Theme.FONT_FAMILY, 11, "bold"),
            bg="#dbeafe",
            fg=Theme.SECONDARY_FG,
            anchor="w",
            padx=10,
            pady=8,
        ).grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(0, 18),
        )

        fields = [
            "First Name",
            "Last Name",
            "Phone",
            "Email",
        ]

        self.entries = {}

        for row, field in enumerate(fields, start=1):
            tk.Label(
                form_frame,
                text=f"{field}:",
                font=(Theme.FONT_FAMILY, 10, "bold"),
                bg=Theme.CARD_BG,
                fg=Theme.TEXT_DARK,
            ).grid(row=row, column=0, sticky="e", padx=(0, 14), pady=8)

            entry = tk.Entry(
                form_frame,
                width=32,
                font=(Theme.FONT_FAMILY, 10),
                relief="solid",
                bd=1,
            )
            entry.grid(row=row, column=1, sticky="ew", pady=8, ipady=5)

            self.entries[field] = entry

        button_frame = tk.Frame(form_frame, bg=Theme.CARD_BG)
        button_frame.grid(
            row=len(fields) + 1,
            column=0,
            columnspan=2,
            pady=(20, 0),
        )

        self._build_button(
            button_frame,
            "Save Member",
            self.add_member,
            bg=Theme.ACCENT,
            fg="white",
            hover_bg=Theme.ACCENT_HOVER,
            width=14,
        ).pack(side="left", padx=6, ipady=4)

        self._build_button(
            button_frame,
            "Back",
            self.create_member_menu,
            bg=Theme.SECONDARY,
            fg=Theme.SECONDARY_FG,
            hover_bg="#bfdbfe",
            width=14,
        ).pack(side="left", padx=6, ipady=4)

    def add_member(self):
        try:
            first_name = self.entries["First Name"].get().strip()
            last_name = self.entries["Last Name"].get().strip()
            phone = self.entries["Phone"].get().strip()
            email = self.entries["Email"].get().strip()

            self.member_service.addMember(
                first_name,
                last_name,
                phone,
                email,
            )

            self.show_dialog(
                "Success",
                "Member added successfully.",
            )

            self.create_member_menu()

        except ValueError as error:
            self.show_dialog(
                "Invalid Member",
                str(error),
            )

        except Exception as error:
            self.show_dialog(
                "Error",
                f"Could not add member.\n\n{error}",
            )

    def show_delete_member_form(self):
        self.clear_view()
        self.configure(bg=Theme.CONTENT_BG)

        tk.Label(
            self,
            text="Delete Member",
            font=(Theme.FONT_FAMILY, 18, "bold"),
            bg=Theme.CONTENT_BG,
            fg=Theme.TEXT_DARK,
        ).pack(pady=(20, 10))

        form_frame = tk.Frame(
            self,
            bg=Theme.CARD_BG,
            highlightbackground=Theme.CARD_BORDER,
            highlightthickness=1,
            padx=28,
            pady=24,
        )
        form_frame.pack(padx=20, pady=(5, 20))

        tk.Label(
            form_frame,
            text="Member Lookup",
            font=(Theme.FONT_FAMILY, 11, "bold"),
            bg="#dbeafe",
            fg=Theme.SECONDARY_FG,
            anchor="w",
            padx=10,
            pady=8,
        ).grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 18))

        tk.Label(
            form_frame,
            text="Member ID:",
            font=(Theme.FONT_FAMILY, 10, "bold"),
            bg=Theme.CARD_BG,
            fg=Theme.TEXT_DARK,
        ).grid(row=1, column=0, padx=(0, 14), pady=8)

        self.member_id_entry = tk.Entry(
            form_frame,
            width=24,
            font=(Theme.FONT_FAMILY, 10),
            relief="solid",
            bd=1,
        )
        self.member_id_entry.grid(row=1, column=1, pady=8, ipady=5)

        button_frame = tk.Frame(form_frame, bg=Theme.CARD_BG)
        button_frame.grid(
            row=2,
            column=0,
            columnspan=2,
            pady=(20, 0),
        )

        self._build_button(
            button_frame,
            "Delete Member",
            self.delete_member,
            bg=Theme.DANGER,
            fg="white",
            hover_bg=Theme.DANGER_HOVER,
            width=14,
        ).pack(side="left", padx=6, ipady=4)

        self._build_button(
            button_frame,
            "Back",
            self.create_member_menu,
            bg=Theme.SECONDARY,
            fg=Theme.SECONDARY_FG,
            hover_bg="#bfdbfe",
            width=14,
        ).pack(side="left", padx=6, ipady=4)

    def delete_member(self):
        try:
            member_id = int(self.member_id_entry.get())

            confirm = self.show_dialog(
                "Confirm Deletion",
                f"Are you sure you want to permanently delete member ID {member_id}?",
                confirm=True,
            )
            if not confirm:
                return

            deleted_rows = self.member_service.removeMember(member_id)
            if deleted_rows == 0:
                self.show_dialog(
                    "Not Found",
                    f"No member with ID {member_id} was found.",
                )
                return

            self.show_dialog(
                "Success",
                "Member deleted successfully.",
            )

            self.create_member_menu()

        except ValueError:
            self.show_dialog(
                "Invalid Input",
                "Enter a valid numeric member ID.",
            )

        except Exception as error:
            self.show_dialog(
                "Error",
                f"Could not delete member.\n\n{error}",
            )

    def show_all_members(self):
        self.clear_view()
        self.configure(bg=Theme.CONTENT_BG)

        tk.Label(
            self,
            text="All Library Members",
            font=(Theme.FONT_FAMILY, 18, "bold"),
            bg=Theme.CONTENT_BG,
            fg=Theme.TEXT_DARK,
        ).pack(pady=(20, 10))

        columns = (
            "member_id",
            "first_name",
            "last_name",
            "email",
            "phone",
        )

        table_card = tk.Frame(
            self,
            bg=Theme.CARD_BG,
            highlightbackground=Theme.CARD_BORDER,
            highlightthickness=1,
            padx=12,
            pady=12,
        )
        table_card.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(5, 10),
        )

        table_style = ttk.Style()
        table_style.configure(
            "Members.Treeview",
            background=Theme.CARD_BG,
            foreground=Theme.TEXT_DARK,
            fieldbackground=Theme.CARD_BG,
            font=(Theme.FONT_FAMILY, 10),
        )
        table_style.configure(
            "Members.Treeview.Heading",
            background="#dbeafe",
            foreground=Theme.SECONDARY_FG,
            font=(Theme.FONT_FAMILY, 10, "bold"),
            relief="flat",
            padding=(8, 7),
        )
        table_style.map(
            "Members.Treeview.Heading",
            background=[("active", "#bfdbfe")],
        )

        tree = ttk.Treeview(
            table_card,
            columns=columns,
            show="headings",
            style="Members.Treeview",
            height=12,
        )

        scrollbar = ttk.Scrollbar(
            table_card,
            orient="vertical",
            command=tree.yview,
        )
        tree.configure(yscrollcommand=scrollbar.set)

        tree.heading("member_id", text="ID")
        tree.heading("first_name", text="First Name")
        tree.heading("last_name", text="Last Name")
        tree.heading("email", text="Email")
        tree.heading("phone", text="Phone")

        tree.column("member_id", width=70, anchor="center")
        tree.column("first_name", width=130, anchor="w")
        tree.column("last_name", width=130, anchor="w")
        tree.column("email", width=180, anchor="w")
        tree.column("phone", width=120, anchor="w")

        tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        table_card.columnconfigure(0, weight=1)
        table_card.rowconfigure(0, weight=1)

        members = self.member_service.getAllMembers()

        for member in members:
            tree.insert(
                "",
                "end",
                values=(
                    member["member_id"],
                    member["first_name"],
                    member["last_name"],
                    member["email"],
                    member["phone"],
                ),
            )

        self._build_button(
            self,
            "Back",
            self.create_member_menu,
            bg=Theme.ACCENT,
            fg="white",
            hover_bg=Theme.ACCENT_HOVER,
            width=14,
        ).pack(pady=(10, 15), ipadx=6, ipady=4)
