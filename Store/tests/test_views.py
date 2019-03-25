from django.test import TestCase, RequestFactory, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


from Store.models import Order, Book, EBook, AudioBook, PaperBook, Author
from Store.forms import OrderForm
from Store.views import CreateOrder
from Store.cart import Cart


class CreateOrderViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        
        
        Order.objects.create(
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

    def setUp(self):
        self.test_user = get_user_model().objects.create_user(
                    email ="test_user@email.email",
                    first_name="test_user_first_name",
                    last_name="test_user_last_name",
                    password="TestPassword12"
                    )



    def test_logged_user_get(self):
        self.client.login(email='test_user@email.email', password='TestPassword12')
        response = self.client.get(reverse('Store:create_order'))

        self.assertEqual(response.status_code, 200)
        

    def test_logged_user_initial_values(self):
        self.client.force_login(self.test_user)
        response = self.client.get(reverse('Store:create_order'))

        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(response.context['order_form'].initial['first_name'], "test_user_first_name")
        self.assertEqual(response.context['order_form'].initial['email'], "test_user@email.email")
        self.assertEqual(response.context['order_form'].initial['street'], None)
        


    def test_anon_user_get(self):
        self.client = Client()
        response = self.client.get(reverse("Store:create_order"))

        self.assertEqual(response.status_code, 200)
        

    def test_anon_user_post(self):
        self.client = Client()
        response = self.client.post(reverse("Store:create_order"))

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'order_form', 'house_number', 'This field is required.')
        self.assertFormError(response, 'order_form', 'email', 'This field is required.')



    def test_uses_correct_template(self):
        response = self.client.get(reverse('Store:create_order'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Store/create_order.html')
         
    


class ChooseAccountMethodVeiwTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email ="test_user@email.email",
            first_name="test_user_first_name",
            last_name="test_user_last_name",
            password="TestPassword12"
            )
        

    def test_redirect_if_logged_in(self):
        self.client.login(username='test_user@email.email', password='TestPassword12')
        response = self.client.get(reverse('Store:choose_account_method'))
        
        self.assertRedirects(response, reverse("Store:create_order"))
    

    def test_anon_user(self):
        self.client = Client()
        response = self.client.get(reverse('Store:choose_account_method'))

        self.assertEqual(response.status_code, 200)
        

    def test_uses_correct_template(self):
        response = self.client.get(reverse('Store:choose_account_method'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Store/choose_account_method.html')
         
    