from pathlib import Path
from tempfile import TemporaryDirectory

from src.database.database_service import DatabaseService
from src.database.library_database import LibraryDatabase


def test_database() -> None:
    # ==========================================================
    # Creates a temporary database and tests the following workflow:
    # add book, add member, checkout book, and return book
    # ==========================================================

    with TemporaryDirectory() as temporary_directory:
        database_path = Path(temporary_directory) / "test_library.db"

        database = LibraryDatabase(str(database_path))
        database.initialize_database()

        service = DatabaseService(database)

        # Add a book
        book_id = service.add_book(
            title="The Hobbit",
            author="J.R.R. Tolkien",
            isbn="9780547928227",
            genre="Fantasy",
        )

        # Add a member
        member_id = service.add_member(
            first_name="Isaac",
            last_name="Garcia",
            phone="317-555-0100",
            email="isaac@example.com",
        )

        # Assert the records were created
        book = service.get_book_by_id(book_id)
        member = service.get_member_by_id(member_id)

        assert book is not None
        assert book["title"] == "The Hobbit"
        assert book["status"] == "AVAILABLE"

        assert member is not None
        assert member["first_name"] == "Isaac"

        # Check out the book
        checkout_id = service.checkout_book(
            book_id=book_id,
            member_id=member_id,
        )

        checked_out_book = service.get_book_by_id(book_id)
        active_checkouts = service.get_active_checkouts()

        assert checked_out_book is not None
        assert checked_out_book["status"] == "CHECKED_OUT"
        assert len(active_checkouts) == 1
        assert active_checkouts[0]["checkout_id"] == checkout_id

        # Return the book
        service.return_book(checkout_id)

        returned_book = service.get_book_by_id(book_id)
        active_checkouts = service.get_active_checkouts()

        assert returned_book is not None
        assert returned_book["status"] == "AVAILABLE"
        assert len(active_checkouts) == 0

        print("All database tests passed successfully!")


if __name__ == "__main__":
    test_database()