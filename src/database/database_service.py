from datetime import date, timedelta
from typing import Any, Optional
from contextlib import closing

from src.database.library_database import LibraryDatabase

# ==========================================================
# This class provides database operations for books, members, and checkouts.
# books: add_book, get_all_books, get_book_by_id, get_available_books, get_checked_out_books, update_book, delete_book, search_books
# members: add_member, get_all_members, get_member_by_id, update_member, delete_member, search_members
# checkouts: checkout_book, return_book, get_active_checkouts, get_overdue_checkouts, get_checkout_history
# ==========================================================


class DatabaseService:

    def __init__(self, database: LibraryDatabase) -> None:
        self.database = database

    # ==========================================================
    # Book operations
    # ==========================================================

    def add_book(
        self,
        title: str,
        author: str,
        isbn: str,
        genre: Optional[str] = None,
    ) -> int:
        query = """
        INSERT INTO books (title, author, isbn, genre, status)
        VALUES (?, ?, ?, ?, 'AVAILABLE');
        """

        return self.database.execute_non_query(
            query,
            (title, author, isbn, genre),
        )

    def get_all_books(self) -> list[dict[str, Any]]:
        query = """
        SELECT book_id, title, author, isbn, genre, status
        FROM books
        ORDER BY title;
        """

        return self.database.execute_query(query)

    def get_book_by_id(self, book_id: int) -> Optional[dict[str, Any]]:
        query = """
        SELECT book_id, title, author, isbn, genre, status
        FROM books
        WHERE book_id = ?;
        """

        results = self.database.execute_query(query, (book_id,))
        return results[0] if results else None

    def get_available_books(self) -> list[dict[str, Any]]:
        query = """
        SELECT book_id, title, author, isbn, genre, status
        FROM books
        WHERE status = 'AVAILABLE'
        ORDER BY title;
        """

        return self.database.execute_query(query)

    def get_checked_out_books(self) -> list[dict[str, Any]]:
        query = """
        SELECT book_id, title, author, isbn, genre, status
        FROM books
        WHERE status = 'CHECKED_OUT'
        ORDER BY title;
        """

        return self.database.execute_query(query)

    def update_book(
        self,
        book_id: int,
        title: str,
        author: str,
        isbn: str,
        genre: Optional[str] = None,
    ) -> None:
        query = """
        UPDATE books
        SET title = ?,
            author = ?,
            isbn = ?,
            genre = ?
        WHERE book_id = ?;
        """

        self.database.execute_non_query(
            query,
            (title, author, isbn, genre, book_id),
        )

    def delete_book(self, book_id: int) -> None:
        query = """
        DELETE FROM books
        WHERE book_id = ?;
        """

        self.database.execute_non_query(query, (book_id,))

    def search_books(self, search_term: str) -> list[dict[str, Any]]:
        query = """
        SELECT book_id, title, author, isbn, genre, status
        FROM books
        WHERE title LIKE ?
           OR author LIKE ?
           OR isbn LIKE ?
           OR genre LIKE ?
        ORDER BY title;
        """

        wildcard = f"%{search_term}%"

        return self.database.execute_query(
            query,
            (wildcard, wildcard, wildcard, wildcard),
        )

    # ==========================================================
    # Member operations
    # ==========================================================

    def add_member(
        self,
        first_name: str,
        last_name: str,
        phone: Optional[str],
        email: str,
    ) -> int:
        query = """
        INSERT INTO members (first_name, last_name, phone, email)
        VALUES (?, ?, ?, ?);
        """

        return self.database.execute_non_query(
            query,
            (first_name, last_name, phone, email),
        )

    def get_all_members(self) -> list[dict[str, Any]]:
        query = """
        SELECT member_id, first_name, last_name, phone, email
        FROM members
        ORDER BY last_name, first_name;
        """

        return self.database.execute_query(query)

    def get_member_by_id(
        self,
        member_id: int,
    ) -> Optional[dict[str, Any]]:
        query = """
        SELECT member_id, first_name, last_name, phone, email
        FROM members
        WHERE member_id = ?;
        """

        results = self.database.execute_query(query, (member_id,))
        return results[0] if results else None

    def update_member(
        self,
        member_id: int,
        first_name: str,
        last_name: str,
        phone: Optional[str],
        email: str,
    ) -> None:
        query = """
        UPDATE members
        SET first_name = ?,
            last_name = ?,
            phone = ?,
            email = ?
        WHERE member_id = ?;
        """

        self.database.execute_non_query(
            query,
            (first_name, last_name, phone, email, member_id),
        )

    def delete_member(self, member_id: int) -> int:
        query = """
        DELETE FROM members
        WHERE member_id = ?;
        """

        return self.database.execute_modify(query, (member_id,))

    def search_members(
        self,
        search_term: str,
    ) -> list[dict[str, Any]]:
        query = """
        SELECT member_id, first_name, last_name, phone, email
        FROM members
        WHERE first_name LIKE ?
           OR last_name LIKE ?
           OR phone LIKE ?
           OR email LIKE ?
        ORDER BY last_name, first_name;
        """

        wildcard = f"%{search_term}%"

        return self.database.execute_query(
            query,
            (wildcard, wildcard, wildcard, wildcard),
        )

    # ==========================================================
    # Checkout operations
    # ==========================================================

    def checkout_book(
        self,
        book_id: int,
        member_id: int,
        checkout_length_days: int = 14,
    ) -> int:

        checkout_date = date.today()
        due_date = checkout_date + timedelta(days=checkout_length_days)

        with closing(self.database.connect()) as connection:
            book = connection.execute(
                """
                SELECT status
                FROM books
                WHERE book_id = ?;
                """,
                (book_id,),
            ).fetchone()

            if book is None:
                raise ValueError(f"Book with ID {book_id} does not exist.")

            if book["status"] != "AVAILABLE":
                raise ValueError("This book is already checked out.")

            member = connection.execute(
                """
                SELECT member_id
                FROM members
                WHERE member_id = ?;
                """,
                (member_id,),
            ).fetchone()

            if member is None:
                raise ValueError(f"Member with ID {member_id} does not exist.")

            cursor = connection.execute(
                """
                INSERT INTO checkouts (
                    book_id,
                    member_id,
                    checkout_date,
                    due_date,
                    return_date
                )
                VALUES (?, ?, ?, ?, NULL);
                """,
                (
                    book_id,
                    member_id,
                    checkout_date.isoformat(),
                    due_date.isoformat(),
                ),
            )

            connection.execute(
                """
                UPDATE books
                SET status = 'CHECKED_OUT'
                WHERE book_id = ?;
                """,
                (book_id,),
            )

            connection.commit()
            return cursor.lastrowid

    def return_book(self, checkout_id: int) -> None:

        return_date = date.today().isoformat()

        with closing(self.database.connect()) as connection:
            checkout = connection.execute(
                """
                SELECT book_id, return_date
                FROM checkouts
                WHERE checkout_id = ?;
                """,
                (checkout_id,),
            ).fetchone()

            if checkout is None:
                raise ValueError(f"Checkout with ID {checkout_id} does not exist.")

            if checkout["return_date"] is not None:
                raise ValueError("This book has already been returned.")

            connection.execute(
                """
                UPDATE checkouts
                SET return_date = ?
                WHERE checkout_id = ?;
                """,
                (return_date, checkout_id),
            )

            connection.execute(
                """
                UPDATE books
                SET status = 'AVAILABLE'
                WHERE book_id = ?;
                """,
                (checkout["book_id"],),
            )

            connection.commit()

    def get_active_checkouts(self) -> list[dict[str, Any]]:
        query = """
        SELECT
            c.checkout_id,
            c.book_id,
            b.title AS book_title,
            c.member_id,
            m.first_name || ' ' || m.last_name AS member_name,
            c.checkout_date,
            c.due_date
        FROM checkouts c
        JOIN books b
            ON c.book_id = b.book_id
        JOIN members m
            ON c.member_id = m.member_id
        WHERE c.return_date IS NULL
        ORDER BY c.due_date;
        """

        return self.database.execute_query(query)

    def get_overdue_checkouts(self) -> list[dict[str, Any]]:
        query = """
        SELECT
            c.checkout_id,
            b.title AS book_title,
            m.first_name || ' ' || m.last_name AS member_name,
            m.email,
            m.phone,
            c.checkout_date,
            c.due_date
        FROM checkouts c
        JOIN books b
            ON c.book_id = b.book_id
        JOIN members m
            ON c.member_id = m.member_id
        WHERE c.return_date IS NULL
          AND c.due_date < ?
        ORDER BY c.due_date;
        """

        return self.database.execute_query(
            query,
            (date.today().isoformat(),),
        )

    def get_checkout_history(self) -> list[dict[str, Any]]:
        query = """
        SELECT
            c.checkout_id,
            b.title AS book_title,
            m.first_name || ' ' || m.last_name AS member_name,
            c.checkout_date,
            c.due_date,
            c.return_date
        FROM checkouts c
        JOIN books b
            ON c.book_id = b.book_id
        JOIN members m
            ON c.member_id = m.member_id
        ORDER BY c.checkout_date DESC;
        """

        return self.database.execute_query(query)
