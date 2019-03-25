from django.test import TestCase
from django.contrib.auth import get_user_model

from Store.models import Order, Book, EBook, AudioBook, PaperBook, Author



class BookModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Book.objects.create(title="Dziady", description="Description")

    def test_book_to_str(self):
        book = Book.objects.get(pk=1)

        self.assertEqual(str(book), "Dziady")


class AuthorModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Author.objects.create(first_name="Adam", last_name="Mickiewicz")
        Author.objects.create(first_name="Adam", second_name="Bernard", last_name="Mickiewicz")


    def test_str_with_only_first_name_and_last_name(self):
        author = Author.objects.get(id=1)
        self.assertEqual(str(author), "Adam Mickiewicz")

    def test_str_withy_first_second_last_name(self):
        author = Author.objects.get(id=2)
        self.assertEqual(str(author), "Adam Bernard Mickiewicz")


