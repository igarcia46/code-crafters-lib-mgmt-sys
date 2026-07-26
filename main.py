from src.database.database_service import DatabaseService
from src.database.library_database import LibraryDatabase
from src.services.BookService import BookService
from src.services.MemberService import MemberService
from src.services.CheckoutService import CheckoutService

from models.Book import Book
from models.Member import Member
from models.Checkout import Checkout

from src.ui.LibraryGUI import LibraryGUI


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

    if len(database_service.get_all_books()) == 0:
        database_service.add_book("The Great Gatsby","F. Scott Fitzgerald", "11111","Fiction")
        database_service.add_book("I Robot","Isaac Asimov","22222","Science Fiction")
        database_service.add_book("The Hobbit","J.R.R. Tolkien","33333", "Fantasy")
    if len(database_service.get_all_members()) ==0:
        database_service.add_member("Jane","Doe","111-111-1111","JaneDoe@gmail.com")
        database_service.add_member("Bob","Doe","222-222-2222","BobDoe@gmail.com")
        database_service.add_member("Sue","Smith","333-333-3333","SueSmith@protonmail.com")

    if len(database_service.get_active_checkouts()) == 0:
        database_service.checkout_book(1, 1)

    # Open GUI
    LibraryGUI(database_service)


if __name__ == "__main__":
    main()
