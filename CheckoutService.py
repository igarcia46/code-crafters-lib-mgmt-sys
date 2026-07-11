import LibraryDatabase
import datetime

class CheckoutService:
    def checkOutBook(book_id, member_id):
        pass

    #PLACEHOLDER
    def returnBook(checkout_id):
        pass
    #PLACEHOLDER

    def getCheckoutHistory(member_id):
        pass
    #PLACEHOLDER

    def getOverdueBooks():
        return LibraryDatabase.executeQuery(f"SELECT * FROM Checkouts WHERE dueDate < {datetime.datetime.now()}", None)
    #PLACEHOLDER
