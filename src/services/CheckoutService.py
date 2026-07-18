from src.database.database_service import DatabaseService

class CheckoutService:
    def __init__(self, database):
        self.database = database

    def checkOutBook(self, book_id, member_id):
        return DatabaseService.checkout_book(self.database, book_id, member_id)

    def returnBook(self, checkout_id):
        return DatabaseService.return_book(self.database, checkout_id)
    
    def getCheckoutHistory(self):
        return DatabaseService.get_checkout_history(self.database)

    def getOverdueBooks(self):
        return DatabaseService.get_overdue_checkouts(self.database)
