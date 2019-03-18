from django.contrib import admin
from .models import Author, Reader, Book, EBook, AudioBook, PaperBook
from .models import Category


@admin.register(Author, Reader)
class PersonAdmin(admin.ModelAdmin):
    pass

@admin.register(Book, EBook, AudioBook, PaperBook, Category)
class BookAdmin(admin.ModelAdmin):
    pass


