from django.contrib import admin
from .models import Author, Reader, Book, EBook, AudioBook, PaperBook

@admin.register(Author, Reader)
class PersonAdmin(admin.ModelAdmin):
    pass

@admin.register(Book, EBook, AudioBook, PaperBook)
class BookAdmin(admin.ModelAdmin):
    pass


