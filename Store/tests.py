from django.test import TestCase

from .models import Order
from .forms import OrderForm

class CreateOrderTest(TestCase):


    def setUp(self):
        user = get_user_model().objects.create_user('test_user')
        self.order = Order.objects.create(
            email = "test@test.pl",
            first_name = "test",
            last_name = "test",
            house_number = "123",
            street = "123",
            city = "Poznan",
            zip_code = "61-288",
            voivodeship = "wielkopolska",
            additional_info = "test info"
        )


    def test_init(self):
        OrderForm(entry=self.entry)

    def test_init_without_entry(self):
        with self.assertRaises(KeyError):
            OrderForm()