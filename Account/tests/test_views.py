from django.test import TestCase, Client
from django.urls import reverse


from Account.models import User
from Account.views import OrderHistory

from Store.models import Order, Book


class OrderHistoryViewTest(TestCase):

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

        self.test_user = User.objects.create_user("test@test.test", "test123")
        self.test_user.orders.add(Order.objects.get(pk=1))


    def test_template_rendered(self):
        self.client.force_login(self.test_user)
        response = self.client.get(reverse('Account:order_history'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Account/order_history.html')
        
    
    def test_client_redirect_anon_user(self):
        self.client = Client()
        response = self.client.get(reverse('Account:order_history')) 
        login_redirect_url = '/accounts/login/?next='+ reverse('Account:order_history')

        self.assertRedirects(response, login_redirect_url)
    

    def test_logged_user(self):
        self.client.force_login(self.test_user)
        response = self.client.get(reverse('Account:order_history'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'test@test.test')
        self.assertQuerysetEqual(response.context['orders'], self.test_user.orders.all(), transform=lambda x: x)
        # IDK how to compare these querysets



class ObservedBooksViewTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        for i in range(5):
            Book.objects.create(title=f'test book {i}')


    def setUp(self):
        self.test_user = User.objects.create_user("test@test.test", "test123")
        self.test_user.observed.set(Book.objects.all())

    def test_template_rendered(self):
        self.client.force_login(self.test_user)
        response = self.client.get(reverse("Account:observed_books"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "Account/observed.html")

    
    def test_redirect_anon_user(self):
        self.client = Client()
        response = self.client.get(reverse("Account:observed_books"))
        redirect_url = '/accounts/login/?next=' + reverse('Account:observed_books')
        self.assertRedirects(response, redirect_url)
        
    
    def test_delete_observed_book(self):
        self.client.force_login(self.test_user)

        response = self.client.get(reverse('Account:observed_books'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['observed'].count(), 5)

        response = self.client.delete(reverse('Account:observed_books', args=[1]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.test_user.observed.count(), 4)


    def test_delete_non_existing_book_from_observed(self):
        self.client.force_login(self.test_user)
        response = self.client.delete(reverse('Account:observed_books', args=[10000000]))

        self.assertEqual(response.status_code, 404)


    def test_observe_book(self):
        self.client.force_login(self.test_user)

        response = self.client.get(reverse('Account:observed_books'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['observed'].count(), 5)

        book = Book.objects.create(title="test book 6")
        response = self.client.post(reverse('Account:observed_books', args=[6]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.test_user.observed.count(), 6)


    def test_psot_non_existing_book_from_observed(self):
        self.client.force_login(self.test_user)
        response = self.client.post(reverse('Account:observed_books', args=[10000000]))

        self.assertEqual(response.status_code, 404)


# TODO
class AccountOptionsViewTest(TestCase):
    pass


# TODO
class SignUpViewTest(TestCase):
    pass


