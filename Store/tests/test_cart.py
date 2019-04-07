from django.test import TestCase, Client

from decimal import Decimal

from Store.cart import Cart
from Store.models import Book, PaperBook, AudioBook, EBook, OrderItem, Order


class CartTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        paper_book = PaperBook.objects.create(price="13.22")
        ebook = EBook.objects.create(price="13.22")
        audio_book = AudioBook.objects.create(price="13.22")
        book = Book.objects.create(title="test", paper_book = paper_book, audio_book=audio_book, ebook=ebook)

        order = Order.objects.create(
            email="test@test.test",
            first_name="test",
            last_name="test",
            house_number="test",
            street="test",
            city="test",
            zip_code="test",    
            voivodeship="test"
            )
        OrderItem.objects.create(order=order, book=book, book_type="paper_book", price=paper_book.price, quantity=1)
        OrderItem.objects.create(order=order, book=book, book_type="ebook", price=ebook.price, quantity=1)
        OrderItem.objects.create(order=order, book=book, book_type="audio_book", price=audio_book.price, quantity=1)
            

    def setUp(self):
        client1 = Client()
        session1 = client1.session
        self.cart_empty = Cart(session1)

        client2 = Client()
        session2 = client2.session
        self.cart_with_items = Cart(session2)  

        book = Book.objects.get(pk=1)
        paper_book = PaperBook.objects.get(pk=1)
        ebook = EBook.objects.get(pk=1)
        audio_book = AudioBook.objects.get(pk=1)

        self.cart_with_items.add_item(book.id, "paper_book", paper_book.price)
        self.cart_with_items.add_item(book.id, "audio_book", audio_book.price)
        self.cart_with_items.add_item(book.id, "ebook", ebook.price)

        client3 = Client()
        session3 = client3.session
        self.cart_with_one_item = Cart(session3)
        self.cart_with_one_item.add_item(book.id, "paper_book", paper_book.price)


    def test_create_cart(self):
        self.assertEqual(self.cart_empty.cart, {})


    def test_add_item_to_cart(self):
        self.assertEqual(self.cart_with_one_item.cart, {"1" : {'paper_book':{'price':"13.22", 'quantity':1 }}})
        
        self.assertEqual(self.cart_with_items.cart, {
            "1":{
                'paper_book': {'price':"13.22", 'quantity':1 },
                'ebook': {'price':"13.22", 'quantity':1},
                'audio_book': {'price':"13.22", 'quantity':1},
                }
            })
        book = Book.objects.get(pk=1)
        ebook = book.ebook
        self.cart_with_items.add_item(book.id, "ebook", ebook.price)
        
        self.assertEqual(self.cart_with_items.cart, {
            "1":{
                'paper_book': {'price':"13.22", 'quantity':1 },
                'ebook': {'price':"13.22", 'quantity':2},
                'audio_book': {'price':"13.22", 'quantity':1},
                }
            })

    def test_add_to_empty_cart(self):
        self.assertEqual(self.cart_empty.cart, {})
        book = Book.objects.get(pk=1)
        paper_book = book.paper_book

        self.cart_empty.add_item(book.id, "paper_book", paper_book.price)
        self.assertEqual(self.cart_empty.cart, {"1":{'paper_book':{'quantity':1, 'price':"13.22"}}})
    

    def test_add_item_to_cart_with_str_pk(self):
        self.assertEqual(self.cart_with_one_item.cart, {"1" : {'paper_book':{'price':"13.22", 'quantity':1 }}})
        book = Book.objects.get(pk=1)
        ebook = book.ebook
        self.cart_with_items.add_item(str(book.id), "ebook", ebook.price)
        
        self.assertEqual(self.cart_with_items.cart, {
            "1":{
                'paper_book': {'price':"13.22", 'quantity':1 },
                'ebook': {'price':"13.22", 'quantity':2},
                'audio_book': {'price':"13.22", 'quantity':1},
                }
            })


    def test_get_total_price_and_quantity(self):
        
        self.assertEqual(self.cart_empty.get_total_price_and_quantity(), ("0", 0))
        self.assertEqual(self.cart_with_one_item.get_total_price_and_quantity(), ("13.22", 1))
        self.assertEqual(self.cart_with_items.get_total_price_and_quantity(), ("39.66", 3))
        
        
    def test_iterator(self):
        
        for item in self.cart_with_one_item:
            self.assertEqual(item['quantity'], 1)
            self.assertEqual(item['book'], Book.objects.get(pk=1))
            self.assertEqual(item['book_type'], PaperBook.objects.get(pk=1))
    
        for i, item in enumerate(self.cart_with_items):
            book_type = None
            if i==0:
                book_type = PaperBook.objects.get(pk=1)
            if i==1:
                book_type = AudioBook.objects.get(pk=1)
            if i==2:
                book_type = EBook.objects.get(pk=1)
            
            self.assertEqual(item['quantity'], 1)
            self.assertEqual(item['book'], Book.objects.get(pk=1))
            self.assertEqual(item['book_type'], book_type )
            self.assertEqual(item['book_type'].price, Decimal("13.22"))
    
        self.assertEqual(i, 2)

    def test_create_order_items(self):
        order = Order.objects.get(pk=1)
        order_items = list(OrderItem.objects.all())
        # TODO: I don't know how to assert if these two are equal, (they are not in order and count doesn't work)
        # get back here in free time
        # self.assertSequenceEqual(self.cart_with_items.create_order_items(order), order_items)