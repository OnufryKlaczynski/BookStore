from django.db.models.query import QuerySet

from decimal import Decimal

from .models import Book, OrderItem, Order


CART = 'cart'


class Cart:

    def __init__(self, session):
        
        self.session = session
        cart = self.session.get(CART, None)
        if not cart:
            self.session[CART] = {}

        self.cart = self.session.get(CART, None)
    

    def add_item(self, book_id, book_type, price, quantity=1):
        book_id = str(book_id)
        price = str(price)
        quantity = int(quantity)
        
        if(quantity == 0):
            return

        if not self.cart.get(book_id, None):
            self.cart[book_id] = {}
    
        if not self.cart[book_id].get(book_type, None):
            self.cart[book_id][book_type] = {'price' : price, 'quantity': 0}

        if(self.cart[book_id][book_type]['quantity'] + quantity < 0):
            raise ValueError
            
        self.cart[book_id][book_type]['quantity'] += quantity
        
        self.save()


    def get_total_price_and_quantity(self):
        """Calculates sum of items without asking database about updates in prices."""
        sum = 0 
        quantity = 0
        for book_id in self.cart.keys():
            for book_type in self.cart[book_id].keys():

                book = self.cart[book_id][book_type]
                sum += Decimal(book['price']) * int(book['quantity'])
                quantity += int(book['quantity'])

        return str(sum), quantity
    

    def __iter__(self):
        """Iterate through cart returning dict with actual database items not stored in cart properties."""
        books = Book.objects.filter(id__in = self.cart.keys())
        for i, book_id in enumerate(self.cart.keys()):
            for book_type in self.cart[book_id].keys():
                book_with_type = getattr(books[i], book_type)
                quantity = self.cart[book_id][book_type]['quantity']
                item = {'quantity':quantity, 'book':books[i], 'book_type':book_with_type}
                yield item


    def create_order_items(self, order):
        """Create order model from items stored in cart, asks databaste for anychange in price"""
        order_items = []
        for book_id in self.cart.keys():
            for book_type in self.cart[book_id].keys():

                book_dict = self.cart[book_id][book_type]
                book = Book.objects.get(pk=book_id)
                book_type_model = getattr(book, book_type)
                price = book_type_model.price
                quantity = int(book_dict['quantity'])
                
                item = OrderItem.objects.create(order=order, book=book, book_type=book_type, price=price, quantity=quantity)
                order_items.append(item)

        return order_items


    def save(self):
        self.session.modified = True

