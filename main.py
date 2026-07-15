from src.database.database_service import DatabaseService
from src.database.library_database import LibraryDatabase


def main() -> None:
    database = LibraryDatabase()
    database.initialize_database()

    database_service = DatabaseService(database)

    print("db initialized successfully")
    print(
        f"books currently stored: {len(database_service.get_all_books())}"
    )  # test connection


if __name__ == "__main__":
    main()
