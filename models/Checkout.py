from datetime import date

class Checkout:
    def __init__(self, checkout_id, book_id, member_id, checkoutDate, dueDate, returnDate):
        self.checkout_id = checkout_id
        self.book_id = book_id
        self.member_id = member_id
        self.checkoutDate = checkoutDate
        self.dueDate = dueDate
        self.returnDate = returnDate

    def calculateDueDate(self):
        return self.returnDate

    def markReturned(self):
        pass
    #PLACEHOLDER

    def isOverdue(self):
        today = date.today()
        if today > self.returnDate:
            return True
        else:
            return False


        