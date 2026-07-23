import tkinter as tk
from tkinter import ttk


class MemberView(tk.Frame):
    def __init__(self, parent, member_service):
        super().__init__(parent)

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

        result = {"confirmed": False}

        tk.Label(
            dialog,
            text=message,
            justify="left",
            wraplength=360,
            padx=25,
            pady=20,
        ).pack()

        button_frame = tk.Frame(dialog)
        button_frame.pack(padx=15, pady=(0, 15))

        def close(confirmed=False):
            result["confirmed"] = confirmed
            dialog.destroy()

        if confirm:
            tk.Button(
                button_frame,
                text="Yes",
                width=10,
                command=lambda: close(True),
            ).pack(side="left", padx=5)
            tk.Button(
                button_frame,
                text="No",
                width=10,
                command=close,
            ).pack(side="left", padx=5)
        else:
            tk.Button(
                button_frame,
                text="OK",
                width=10,
                command=close,
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

    def create_member_menu(self):
        self.clear_view()

        tk.Label(
            self,
            text="Member Management",
            font=("Arial", 20, "bold"),
        ).pack(pady=20)

        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        tk.Button(
            button_frame,
            text="Add Member",
            command=self.show_add_member_form,
            width=18,
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            button_frame,
            text="View Members",
            command=self.show_all_members,
            width=18,
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            button_frame,
            text="Delete Member",
            command=self.show_delete_member_form,
            width=18,
        ).grid(row=0, column=2, padx=5)

    def show_add_member_form(self):
        self.clear_view()

        tk.Label(
            self,
            text="Add Member",
            font=("Arial", 18, "bold"),
        ).pack(pady=20)

        form_frame = tk.Frame(
            self,
            bg="white",
            bd=1,
            relief="solid",
            padx=28,
            pady=24,
        )
        form_frame.pack(padx=20, pady=(5, 20))
        form_frame.columnconfigure(1, weight=1)

        tk.Label(
            form_frame,
            text="Member Details",
            font=("Arial", 11, "bold"),
            bg="#d7e3f1",
            fg="#1f2933",
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
                font=("Arial", 10, "bold"),
                bg="white",
                fg="#1f2933",
            ).grid(row=row, column=0, sticky="e", padx=(0, 14), pady=8)

            entry = tk.Entry(
                form_frame,
                width=32,
                font=("Arial", 10),
                relief="solid",
                bd=1,
            )
            entry.grid(row=row, column=1, sticky="ew", pady=8, ipady=5)

            self.entries[field] = entry

        button_frame = tk.Frame(form_frame, bg="white")
        button_frame.grid(
            row=len(fields) + 1,
            column=0,
            columnspan=2,
            pady=(20, 0),
        )

        tk.Button(
            button_frame,
            text="Save Member",
            command=self.add_member,
            width=14,
            font=("Arial", 11, "bold"),
            bg="#2f6fad",
            fg="white",
            activebackground="#245a8d",
            activeforeground="white",
            cursor="hand2",
        ).pack(side="left", padx=6, ipady=4)

        tk.Button(
            button_frame,
            text="Back",
            command=self.create_member_menu,
            width=14,
            font=("Arial", 11, "bold"),
            bg="#d7e3f1",
            fg="#1f2933",
            activebackground="#bdd0e5",
            activeforeground="#1f2933",
            cursor="hand2",
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

        tk.Label(
            self,
            text="Delete Member",
            font=("Arial", 18, "bold"),
        ).pack(pady=20)

        form_frame = tk.Frame(
            self,
            bg="white",
            bd=1,
            relief="solid",
            padx=28,
            pady=24,
        )
        form_frame.pack(padx=20, pady=(5, 20))

        tk.Label(
            form_frame,
            text="Member Lookup",
            font=("Arial", 11, "bold"),
            bg="#d7e3f1",
            fg="#1f2933",
            anchor="w",
            padx=10,
            pady=8,
        ).grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 18))

        tk.Label(
            form_frame,
            text="Member ID:",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#1f2933",
        ).grid(row=1, column=0, padx=(0, 14), pady=8)

        self.member_id_entry = tk.Entry(
            form_frame,
            width=24,
            font=("Arial", 10),
            relief="solid",
            bd=1,
        )
        self.member_id_entry.grid(row=1, column=1, pady=8, ipady=5)

        button_frame = tk.Frame(form_frame, bg="white")
        button_frame.grid(
            row=2,
            column=0,
            columnspan=2,
            pady=(20, 0),
        )

        tk.Button(
            button_frame,
            text="Delete Member",
            command=self.delete_member,
            width=14,
            font=("Arial", 11, "bold"),
            bg="#d9534f",
            fg="white",
            activebackground="#c9302c",
            activeforeground="white",
            cursor="hand2",
        ).pack(side="left", padx=6, ipady=4)

        tk.Button(
            button_frame,
            text="Back",
            command=self.create_member_menu,
            width=14,
            font=("Arial", 11, "bold"),
            bg="#d7e3f1",
            fg="#1f2933",
            activebackground="#bdd0e5",
            activeforeground="#1f2933",
            cursor="hand2",
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

        tk.Label(
            self,
            text="All Library Members",
            font=("Arial", 18, "bold"),
        ).pack(pady=15)

        columns = (
            "member_id",
            "first_name",
            "last_name",
            "email",
            "phone",
        )

        table_frame = tk.Frame(self)
        table_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10,
        )

        table_style = ttk.Style(self)
        table_style.configure(
            "Members.Treeview.Heading",
            background="#d7e3f1",
            foreground="#1f2933",
            font=("Arial", 10, "bold"),
            relief="raised",
            borderwidth=1,
            padding=(8, 7),
        )
        table_style.map(
            "Members.Treeview.Heading",
            background=[("active", "#bdd0e5")],
        )

        tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            style="Members.Treeview",
        )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=tree.yview,
        )
        tree.configure(yscrollcommand=scrollbar.set)

        tree.heading("member_id", text="ID")
        tree.heading("first_name", text="First Name")
        tree.heading("last_name", text="Last Name")
        tree.heading("email", text="Email")
        tree.heading("phone", text="Phone")

        tree.pack(
            side="left",
            fill="both",
            expand=True,
        )
        scrollbar.pack(side="right", fill="y")

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

        tk.Button(
            self,
            text="Back",
            command=self.create_member_menu,
            width=14,
            font=("Arial", 11, "bold"),
            bg="#2f6fad",
            fg="white",
            activebackground="#245a8d",
            activeforeground="white",
            cursor="hand2",
        ).pack(pady=(10, 15), ipadx=6, ipady=4)
