from django.test import TestCase, RequestFactory, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

import json

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

        self.data_of_existing_user = {
            "email": "test@test.pl",
            "first_name": "test",
            "last_name": "test",
            "house_number": "123",
            "street": "123",
            "city": "Poznan",
            "zip_code": "61-288",
            "voivodeship": "wielkopolska",
            "additional_info": "test info"
        }

        self.data_of_anon_user ={
            "email": "unique@test.test",
            "first_name": "test",
            "last_name": "test",
            "house_number": "123",
            "street": "123",
            "city": "Poznan",
            "zip_code": "61-288",
            "voivodeship": "wielkopolska",
            "additional_info": "test info"
        }
        

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


    def test_post_with_no_data_for_logged_user(self):
        self.client.force_login(self.test_user)
        
        self.assertEqual(len(Order.objects.all()), 1)
        response = self.client.post(reverse('Store:create_order'), )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Order.objects.all()), 1)

        
    def test_order_creation_looged_user(self):
        self.client.force_login(self.test_user)
        
        self.assertEqual(len(Order.objects.all()), 1)
        response = self.client.post(reverse('Store:create_order'), self.data_of_existing_user )
        self.assertRedirects(response, reverse('Store:order_confirmation'))
        self.assertEqual(len(Order.objects.all()), 2)
        self.assertEqual(self.test_user.orders.all()[0], Order.objects.all()[1])
        

        
    def test_anon_user_get(self):
        self.client = Client()
        response = self.client.get(reverse("Store:create_order"), )

        self.assertEqual(response.status_code, 200)
        

    def test_anon_user_post_with_no_data(self):
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
         

class AddToCartViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        paper_book = PaperBook.objects.create(price=13.22)
        audio_book = AudioBook.objects.create(price=13.22)
        ebook = EBook.objects.create(price=13.22)
        Book.objects.create(
            title="Dziady",
            paper_book=paper_book,
            audio_book=audio_book,
            ebook=ebook
            )

    def setUp(self):
        self.valid_data = json.dumps({
            "id" : 1,
            "type": "paper_book",
            "quantity" : 1,
        
        })
        self.valid_data2 = json.dumps({
            "id" : 1,
            "type": "audio_book",
            "quantity" : 1,
        
        })
        self.valid_data3 = json.dumps({
            "id" : 1,
            "type": "ebook",
            "quantity" : 1,
        
        })

        self.invalid_id  = json.dumps({
            "id" : 123,
            "type": "ebook",
            "quantity" : 1,
        
        })
        self.invalid_id2  = json.dumps({
            "id" : -12,
            "type": "ebook",
            "quantity" : 1,
        
        })
        self.invalid_id3  = json.dumps({
            "id" : "",
            "type": "ebook",
            "quantity" : 1,
        
        })
        self.invalid_type  = json.dumps({
            "id" : 1,
            "type": "e_book",
            "quantity" : 1,
        
        })
        self.invalid_type2  = json.dumps({
            "id" : 1,
            "type": "",
            "quantity" : 1,
        
        })
        self.empty_data = json.dumps({
            "id":"",
            "type":"",
            "quantity" : 1,
        })

        self.empty_data2 = json.dumps({
            "id":None,
            "type":None,
            "quantity" : 1,
        })

        self.invalid_quantity = json.dumps({
            "id":None,
            "type":None,
            "quantity" : None,
        })

    def test_response_for_valid_data(self):
        session = self.client.session
        cart= Cart(session).cart
        self.assertEqual(cart, {})
        
        response = self.client.post(reverse("Store:add_to_cart"), self.valid_data, content_type="application/json")
        session = self.client.session
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['status'], "ok")
    
        cart = Cart(session).cart
        
        self.assertEqual(cart, {"1":{"paper_book": {"quantity":1, "price":"13.22"}}})
        


    def test_response_for_invalid_id(self):
        response = self.client.post(reverse("Store:add_to_cart"), self.invalid_id, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['status'], "error")
        self.assertEqual(json.loads(response.content)['error_msg'], "object does not exist")
        
        response = self.client.post(reverse("Store:add_to_cart"), self.invalid_id2, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['status'], "error")
        self.assertEqual(json.loads(response.content)['error_msg'], "object does not exist")
        
        response = self.client.post(reverse("Store:add_to_cart"), self.invalid_id3, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['status'], "error")
        self.assertEqual(json.loads(response.content)['error_msg'], "invalid data type")
    
    
    def test_response_for_invalid_book_type(self):
        response = self.client.post(reverse("Store:add_to_cart"), self.invalid_type, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['status'], "error")
        self.assertEqual(json.loads(response.content)['error_msg'], "invalid book type")
        
        response = self.client.post(reverse("Store:add_to_cart"), self.invalid_type2, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['status'], "error")
        self.assertEqual(json.loads(response.content)['error_msg'], "invalid book type")
    

    def test_response_for_empty_data(self):
        response = self.client.post(reverse("Store:add_to_cart"), self.empty_data, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['status'], "error")
        self.assertEqual(json.loads(response.content)['error_msg'], "invalid data type")
        
        response = self.client.post(reverse("Store:add_to_cart"), self.empty_data2, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['status'], "error")
        self.assertEqual(json.loads(response.content)['error_msg'], "invalid data type")

        response = self.client.post(reverse("Store:add_to_cart"), self.invalid_quantity, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['status'], "error")
        self.assertEqual(json.loads(response.content)['error_msg'], "invalid data type")
        

