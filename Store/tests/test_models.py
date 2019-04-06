from django.test import TestCase
from django.contrib.auth import get_user_model

from Store.models import Order, Book, EBook, AudioBook, PaperBook, Author



class BookModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        paper_book = PaperBook.objects.create(price=19.22)
        audio_book = AudioBook.objects.create(price=19.22)
        ebook = EBook.objects.create(price=19.22)
        Book.objects.create(title="Dziady", paper_book=paper_book, description="Description")
        Book.objects.create(title="Dziady2", audio_book=audio_book, description="Description2")
        Book.objects.create(title="Dziady3", ebook=ebook, description="Description3")
        Book.objects.create(title="Dziady4", description="Description4 ")

    def test_book_to_str(self):
        book = Book.objects.get(pk=1)

        self.assertEqual(str(book), "Dziady")

    def test_get_first_available_type(self):
        paper_book = Book.objects.get(pk=1).first_available_type
        self.assertEqual(paper_book, PaperBook.objects.get(pk=1))
        
        audio_book = Book.objects.get(pk=2).first_available_type
        self.assertEqual(audio_book, AudioBook.objects.get(pk=1))
        
        ebook = Book.objects.get(pk=3).first_available_type
        self.assertEqual(ebook, EBook.objects.get(pk=1))

        self.assertEqual(Book.objects.get(pk=4).first_available_type, None)

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


