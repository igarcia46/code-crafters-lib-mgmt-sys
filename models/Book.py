from src.database.database_service import DatabaseService

class Book:
    def __init__(self, book_id, title, author, isbn, genre, status):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.isbn = isbn
        self.genre = genre
        self.status = status

    def getBookInfo(self):
        return [self.book_id, self.title, self.author, self.isbn, self.genre, self.status]

    def updateStatus(self):
        if(self.status == "AVAILABLE"):
            self.status = "CHECKED_OUT"
        elif(self.status == "CHECKED_OUT"):
            self.status = "AVAILABLE"
    #PLACEHOLDER