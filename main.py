from src.database.database_service import DatabaseService
from src.database.library_database import LibraryDatabase
from src.services.BookService import BookService

from models.Book import Book


def main() -> None:
    database = LibraryDatabase()
    database.initialize_database()

    database_service = DatabaseService(database)

    book_service = BookService(database_service)

    print("db initialized successfully")
    print(
        f"books currently stored: {len(database_service.get_all_books())}"
    )  # test connection
    book_service.addBook("Test Book","Jane Doe","12345", "Genre")
    book_service.updateBook(1, "Test Book Update","Jane Doe","8765", "Genre")
    print(book_service.getBookById(1))
    print(book_service.checkAvailability(1))
    #book_service.removeBook(1)

    testBookQuery = book_service.getBookById(1)

    #creating a book object
    testBook = Book(testBookQuery["book_id"], 
                    testBookQuery["title"],
                    testBookQuery["author"],
                    testBookQuery["isbn"],
                    testBookQuery["genre"],
                    testBookQuery["status"])
    
    #print the test book object before and after updating status
    print(testBook.getBookInfo())
    testBook.updateStatus()
    print(testBook.getBookInfo())




if __name__ == "__main__":
    main()
