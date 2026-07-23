
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

    def show_edit(self): self._placeholder("Edit Book")
    def show_delete(self): self._placeholder("Delete Book")
    def show_search(self): self._placeholder("Search Book")
    def show_availability(self): self._placeholder("Availability")
