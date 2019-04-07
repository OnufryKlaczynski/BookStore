from django.test import TestCase
from django.contrib.auth import get_user_model

from Store.models import Order, Book, EBook, AudioBook, PaperBook, Author
from Store.forms import OrderForm

class OrderCreateFormTest(TestCase):
    
    def setUp(self):
        self.test_order_full = {
            "email" : "test@test.pl",
            "first_name" : "test",
            "last_name" : "test",
            "house_number" : "123",
            "street" : "123",
            "city" : "Poznan",
            "zip_code" : "61-288",
            "voivodeship" : "wielkopolska",
            "additional_info" : "test info"
        }

        self.test_order_full_without_additional_info = {
            "email" : "test@test.pl",
            "first_name" : "test",
            "last_name" : "test",
            "house_number" : "123",
            "street" : "123",
            "city" : "Poznan",
            "zip_code" : "61-288",
            "voivodeship" : "wielkopolska",
            
        }

        self.test_order_balnk = {
            "email" : "test@test.pl",
            "first_name" : "test",
            "last_name" : "test",
            "house_number" : "123",
            # "street" : "123",
            # "city" : "Poznan",
            "zip_code" : "61-288",
            "voivodeship" : "wielkopolska",
            "additional_info" : "test info"
        }

    
    def test_full_information_form(self):
        order_form = OrderForm(data=self.test_order_full)

        self.assertTrue(order_form.is_valid())


    def test_not_full_information(self):
        order_form = OrderForm(data=self.test_order_balnk)

        self.assertFalse(order_form.is_valid())


    def test_if_additionl_info_not_required(self):
        order_form = OrderForm(data=self.test_order_full_without_additional_info)

        self.assertTrue(order_form.is_valid())
    