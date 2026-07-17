from src.database.database_service import DatabaseService

class BookService:
    def __init__(self, database):
        self.database = database

    def addBook(self, title, author, isbn, genre):
        #first arguement should be the database object
        return DatabaseService.add_book(self.database, title, author, isbn, genre)

    def updateBook(self, book_id, title, author, isbn, genre):
        return DatabaseService.update_book(self.database, book_id, title, author, isbn, genre)

    def removeBook(self, book_id):
        return DatabaseService.delete_book(self.database,book_id)

    def searchBook(self, search_term):
        return DatabaseService.search_books(self.database,search_term)
    
    def getBookById(self, book_id):
        return DatabaseService.get_book_by_id(self.database, book_id)

    def checkAvailability(self, book_id):
        book = DatabaseService.get_book_by_id(self.database, book_id)
        if(book["status"]) == "AVAILABLE":
            return True
        else:
            return False