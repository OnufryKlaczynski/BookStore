from decimal import Decimal

from .models import Book

CART = 'cart'

class Cart:

    def __init__(self, request):
        self.request = request
        self.session = request.session
        cart = self.session.get(CART, None)
        if not cart:
            self.session[CART] = {}

        self.cart = self.session.get(CART, None)
    

    def add_item(self, book_id, book_type, price):
        
        if not self.cart.get(book_id, None):
            self.cart[book_id] = {}
    
        if not self.cart[book_id].get(book_type, None):
            self.cart[book_id][book_type] = {'price' : price, 'quantity': 0}

        self.cart[book_id][book_type]['quantity'] += 1

        self.save()


    def get_total_price(self):
        """Calculates sum of items without asking database about updates in prices."""
        sum = 0 
        for book_id in self.cart.keys():
            for book_type in self.cart[book_id].keys():

                book = self.cart[book_id][book_type]
                sum += Decimal(book['price']) * int(book['quantity'])

        return str(sum)
    

    def recalculates_prices(self):
        """Asks database for the updated in prices."""
        pass


    def __iter__(self):
        books = Book.objects.filter(id__in = self.cart.keys())
        for i, book_id in enumerate(self.cart.keys()):
            for book_type in self.cart[book_id].keys():
                book_with_type = getattr(books[i], book_type)
                quantity = self.cart[book_id][book_type]['quantity']
                item = {'quantity':quantity, 'book':books[i], 'book_type':book_with_type}
                yield item



    def save(self):
        self.session.modified = True



class BookInfo():

    def __ini__(self, book_id, book_type, quantity):
        self.book_id = book_id
        self.book_type = book_type
        self.quantity = quantity