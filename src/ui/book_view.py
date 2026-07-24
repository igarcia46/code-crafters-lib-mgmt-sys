
import tkinter as tk
from tkinter import ttk, messagebox

class BookView(tk.Frame):
    def __init__(self,parent,book_service):
        super().__init__(parent,bg="#f3f4f6")
        self.book_service=book_service
        self.create_menu()

    def clear(self):
        for w in self.winfo_children():
            w.destroy()

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

    def create_menu(self):
        self.clear()
        tk.Label(self,text="Book Management",font=("Segoe UI",20,"bold"),bg="#f3f4f6").pack(pady=20)
        for txt,cmd in [
            ("Add Book",self.show_add),
            ("View Books",self.show_books),
            ("Edit Book",self.show_edit),
            ("Delete Book",self.show_delete),
            ("Search Book",self.show_search),
            ("Availability",self.show_availability)
        ]:
            tk.Button(self,text=txt,width=25,bg="#2563eb",fg="white",command=cmd).pack(pady=5)

    def show_add(self):
        self.clear()
        tk.Label(self,text="Add Book",font=("Segoe UI",18,"bold"),bg="#f3f4f6").pack(pady=10)
        frm=tk.Frame(self,bg="white",padx=20,pady=20)
        frm.pack()
        self.e={}
        for i,n in enumerate(["Title","Author","ISBN","Genre"]):
            tk.Label(frm,text=n,bg="white").grid(row=i,column=0,sticky="e",padx=5,pady=5)
            en=tk.Entry(frm,width=35)
            en.grid(row=i,column=1,pady=5)
            self.e[n]=en
        tk.Button(frm,text="Save",command=self.add).grid(row=5,column=0,pady=10)
        tk.Button(frm,text="Back",command=self.create_menu).grid(row=5,column=1)

    def add(self):
        try:
            self.book_service.addBook(self.e["Title"].get(),self.e["Author"].get(),self.e["ISBN"].get(),self.e["Genre"].get())
            messagebox.showinfo("Success","Book added.")
        except Exception as ex:
            messagebox.showerror("Error",str(ex))

    def show_books(self):
        self.clear()
        tk.Label(self,text="Books",font=("Segoe UI",18,"bold"),bg="#f3f4f6").pack()
        cols=("ID","Title","Author","ISBN","Genre","Status")
        tree=ttk.Treeview(self,columns=cols,show="headings")
        for c in cols:
            tree.heading(c,text=c)
        tree.pack(fill="both",expand=True,padx=20,pady=20)
        try:
            for b in self.book_service.getAllBooks():
                tree.insert("",tk.END,values=(b["book_id"],b["title"],b["author"],b["isbn"],b["genre"],b["status"]))
        except:
            pass
        tk.Button(self,text="Back",command=self.create_menu).pack()

    def _placeholder(self,title):
        self.clear()
        tk.Label(self,text=title,font=("Segoe UI",18,"bold"),bg="#f3f4f6").pack(pady=20)
        tk.Label(self,text="Connect this page to your BookService.",bg="#f3f4f6").pack()
        tk.Button(self,text="Back",command=self.create_menu).pack(pady=20)

    def show_edit(self):
        self.clear()
    
        tk.Label(
                self,
                text="Edit Book",
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
                text="Book Lookup",
                font=("Arial", 11, "bold"),
                bg="#d7e3f1",
                fg="#1f2933",
                anchor="w",
                padx=10,
                pady=8,
            ).grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 18))
    
        tk.Label(
                form_frame,
                text="Book ID:",
                font=("Arial", 10, "bold"),
                bg="white",
                fg="#1f2933",
            ).grid(row=1, column=0, padx=(0, 14), pady=8)
    
        self.book_id_entry = tk.Entry(
                form_frame,
                width=24,
                font=("Arial", 10),
                relief="solid",
                bd=1,
            )
        self.book_id_entry.grid(row=1, column=1, pady=8, ipady=5)
    
        button_frame = tk.Frame(form_frame, bg="white")
        button_frame.grid(
                row=2,
                column=0,
                columnspan=2,
                pady=(20, 0),
            )
    
        tk.Button(
                button_frame,
                text="Search by ID",
                command=self.edit_entries,
                width=14,
                font=("Arial", 11, "bold"),
                bg="#215e26",
                fg="white",
                activebackground="#215e26",
                activeforeground="white",
                cursor="hand2",
            ).pack(side="left", padx=6, ipady=4)
    
        tk.Button(
                button_frame,
                text="Back",
                command=self.create_menu,
                width=14,
                font=("Arial", 11, "bold"),
                bg="#d7e3f1",
                fg="#1f2933",
                activebackground="#bdd0e5",
                activeforeground="#1f2933",
                cursor="hand2",
            ).pack(side="left", padx=6, ipady=4)

        frm=tk.Frame(self,bg="white",padx=20,pady=20)
        frm.pack()
        #self.e={}
        #for i,n in enumerate(["Title","Author","ISBN","Genre"]):
        #    tk.Label(frm,text=n,bg="white").grid(row=i,column=0,sticky="e",padx=5,pady=5)
            
        self.title_entry = tk.Entry(frm, width = 35)
        self.title_entry.grid(row = 0, column = 1, pady=5)
        self.author_entry = tk.Entry(frm, width = 35)
        self.author_entry.grid(row = 1, column = 1, pady=5)
        self.isbn_entry = tk.Entry(frm, width = 35)
        self.isbn_entry.grid(row = 2, column = 1, pady=5)
        self.genre_entry = tk.Entry(frm, width = 35)
        self.genre_entry.grid(row = 3, column = 1, pady=5)
        
        tk.Button(frm,text="Save",command=self.edit_book).grid(row=5,column=0,pady=10)
        tk.Button(frm,text="Back",command=self.create_menu).grid(row=5,column=1)

    def edit_entries(self):
        try:
            book_id = int(self.book_id_entry.get())
            book = self.book_service.getBookById(book_id)
    
            print(book["title"])
            self.title_entry.delete(0, tk.END)
            self.author_entry.delete(0, tk.END)
            self.isbn_entry.delete(0, tk.END)
            self.genre_entry.delete(0, tk.END)

            print(book["title"])

            self.title_entry.insert(0, book["title"])
            self.author_entry.insert(0, book["author"])
            self.isbn_entry.insert(0, book["isbn"])
            self.genre_entry.insert(0, book["genre"])
        
        except:
            pass

    def edit_book(self):
        try:
            self.book_service.updateBook(self.title_entry.get(),self.author_entry.get(),self.isbn_entry.get(),self.genre_entry.get())
            messagebox.showinfo("Success","Book updated.")
        except Exception as ex:
            messagebox.showerror("Error",str(ex))

    def show_delete(self): 
        self.clear()
    
        tk.Label(
                self,
                text="Delete Book",
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
                text="Book Lookup",
                font=("Arial", 11, "bold"),
                bg="#d7e3f1",
                fg="#1f2933",
                anchor="w",
                padx=10,
                pady=8,
            ).grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 18))
    
        tk.Label(
                form_frame,
                text="Book ID:",
                font=("Arial", 10, "bold"),
                bg="white",
                fg="#1f2933",
            ).grid(row=1, column=0, padx=(0, 14), pady=8)
    
        self.book_id_entry = tk.Entry(
                form_frame,
                width=24,
                font=("Arial", 10),
                relief="solid",
                bd=1,
            )
        self.book_id_entry.grid(row=1, column=1, pady=8, ipady=5)
    
        button_frame = tk.Frame(form_frame, bg="white")
        button_frame.grid(
                row=2,
                column=0,
                columnspan=2,
                pady=(20, 0),
            )
    
        tk.Button(
                button_frame,
                text="Delete Book",
                command=self.delete_book,
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
                command=self.create_menu,
                width=14,
                font=("Arial", 11, "bold"),
                bg="#d7e3f1",
                fg="#1f2933",
                activebackground="#bdd0e5",
                activeforeground="#1f2933",
                cursor="hand2",
            ).pack(side="left", padx=6, ipady=4)

    def delete_book(self):
        print("click")
        try:
            book_id = int(self.book_id_entry.get())
            print(book_id)
            confirm = self.show_dialog(
                "Confirm Deletion",
                f"Are you sure you want to permanently delete book ID {book_id}?",
                confirm=True,
            )
            if not confirm:
                print("not confirm")
                return
    
            deleted_rows = self.book_service.removeBook(book_id)
            print(deleted_rows)
            if deleted_rows == 0:
                self.show_dialog(
                    "Not Found",
                    f"No book with ID {book_id} was found.",
                )
                return
    
            self.show_dialog(
                    "Success",
                    "Member deleted successfully.",
                )
    
            self.show_delete()
    
        except ValueError:
            self.show_dialog(
                    "Invalid Input",
                    "Enter a valid numeric book ID.",
                )
    
        except Exception as error:
            self.show_dialog(
                    "Error",
                    f"Could not delete book.\n\n{error}",
                )
    

    def show_search(self): self._placeholder("Search Book")
    def show_availability(self): self._placeholder("Availability")
