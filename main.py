from src.database.database_service import DatabaseService
from src.database.library_database import LibraryDatabase
from src.services.BookService import BookService
from src.services.MemberService import MemberService
from src.services.CheckoutService import CheckoutService

from models.Book import Book
from models.Member import Member
from models.Checkout import Checkout

from LibraryGUI import LibraryGUI

def main() -> None:
    database = LibraryDatabase()
    database.initialize_database()

    database_service = DatabaseService(database)

    book_service = BookService(database_service)
    member_service = MemberService(database_service)
    checkout_service = CheckoutService(database_service)

    print("db initialized successfully")
    print(
        f"books currently stored: {len(database_service.get_all_books())}"
    )  # test connection

    #testing book service
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

    #testing memember service
    member_service.addMember("Jane","Doe", "123-456-7890", "test@gmail.com")
    member_service.updateMember(1, "Jane","Doe","098-765-4321","test@gmail.com")
    print(member_service.getMemberById(1))

    #creating a member object
    testMemberQuery = member_service.getMemberById(1)
    testMember = Member(testMemberQuery["member_id"],
                        testMemberQuery["first_name"],
                        testMemberQuery["last_name"],
                        testMemberQuery["email"],
                        testMemberQuery["phone"])
    print(testMember)
    testMember.update_member("Jane","Doe","123-456-7890","test@gmail.com")
    print(testMember.phone)

    #checkout_service.checkOutBook(1,1)
    #print(checkout_service.getCheckoutHistory())
    #checkout_service.returnBook(1)
    #print(checkout_service.getCheckoutHistory())

    #Open GUI
    LibraryGUI(database_service)
    





if __name__ == "__main__":
    main()
