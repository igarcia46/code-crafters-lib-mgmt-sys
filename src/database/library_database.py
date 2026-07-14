import sqlite3
from contextlib import closing
from pathlib import Path
from typing import Any, Optional


class LibraryDatabase:
    """
    Manages SQLite database connections and schema creation.
    """

    def __init__(self, database_path: Optional[str] = None) -> None:
        if database_path is None:
            project_root = Path(__file__).resolve().parents[2]
            database_path = str(project_root / "data" / "library.db")

        self.database_path = database_path

        # Ensure the directory containing the database exists.
        Path(self.database_path).parent.mkdir(parents=True, exist_ok=True)

    def connect(self) -> sqlite3.Connection:
        """
        Creates and returns a configured SQLite connection.

        The caller is responsible for closing the connection.
        """

        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")

        return connection

    def execute_query(
        self,
        query: str,
        parameters: tuple[Any, ...] = (),
    ) -> list[dict[str, Any]]:
        """
        Executes a SELECT query and returns rows as dictionaries.
        """

        with closing(self.connect()) as connection:
            cursor = connection.execute(query, parameters)
            rows = cursor.fetchall()

            return [dict(row) for row in rows]

    def execute_non_query(
        self,
        query: str,
        parameters: tuple[Any, ...] = (),
    ) -> int:
        """
        Executes an INSERT, UPDATE, or DELETE statement.

        Returns the ID of an inserted record when applicable.
        """

        with closing(self.connect()) as connection:
            try:
                cursor = connection.execute(query, parameters)
                connection.commit()
                return cursor.lastrowid
            except Exception:
                connection.rollback()
                raise

    def initialize_database(self) -> None:
        """
        Creates all required database tables and indexes.
        """

        create_books_table = """
        CREATE TABLE IF NOT EXISTS books (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            isbn TEXT NOT NULL UNIQUE,
            genre TEXT,
            status TEXT NOT NULL DEFAULT 'AVAILABLE'
                CHECK (status IN ('AVAILABLE', 'CHECKED_OUT'))
        );
        """

        create_members_table = """
        CREATE TABLE IF NOT EXISTS members (
            member_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            phone TEXT,
            email TEXT NOT NULL UNIQUE
        );
        """

        create_checkouts_table = """
        CREATE TABLE IF NOT EXISTS checkouts (
            checkout_id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER NOT NULL,
            member_id INTEGER NOT NULL,
            checkout_date TEXT NOT NULL,
            due_date TEXT NOT NULL,
            return_date TEXT,
            FOREIGN KEY (book_id)
                REFERENCES books(book_id)
                ON DELETE RESTRICT,
            FOREIGN KEY (member_id)
                REFERENCES members(member_id)
                ON DELETE RESTRICT
        );
        """

        create_active_checkout_index = """
        CREATE UNIQUE INDEX IF NOT EXISTS idx_one_active_checkout_per_book
        ON checkouts(book_id)
        WHERE return_date IS NULL;
        """

        with closing(self.connect()) as connection:
            try:
                connection.execute(create_books_table)
                connection.execute(create_members_table)
                connection.execute(create_checkouts_table)
                connection.execute(create_active_checkout_index)
                connection.commit()
            except Exception:
                connection.rollback()
                raise
