from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.http.response import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

import json

from .models import Book, Author, Reader, Category, Tag
from .cart import CART, Cart
from .forms import OrderForm



class Index(View):
    
    def get(self, request):
        books = Book.objects.all()
        paginator = Paginator(books, 12)
        page = request.GET.get('page')
        books_page = paginator.get_page(page)

        categories = Category.objects.all()

        return render(request, 'Store/index.html', 
                {
                'books': books_page, 
                'categories':categories,
                })


class BookDetail(View):
    def get(self, request, pk, slug):
        book = get_object_or_404(Book, pk=pk)
        other_books = [other_book for other_book in book.authors.all()[0].books.all() if other_book.pk != book.pk ] 
        print(other_books)
        return render(request, 'Store/book_detail.html', {'book':book, 'other_books':other_books})



class AuthorIndex(View):

    def get(self, request):
        authors = Author.objects.all()

        return render(request, 'Store/author_index.html', {'authors':authors})


class AuthorDetail(View):

    def get(self, request, pk):

        author = get_object_or_404(Author, pk=pk)
        books = author.books.all()
        return render(request, 'Store/author_detail.html', {'author': author, 'books':books})



class DisplayCart(View):

    def get(self, request):
        cart = Cart(request)
        
        return render(request, 'Store/display_cart.html', {'cart':cart})

    def post(self, request):
        cart = Cart(request)
        
        return redirect('Store:choose_account_method')


class ChooseAccountMethod(View):
    def get(self, request):
        if request.user.is_authenticated:
            pass

        return render(request, 'Store/choose_account_method.html', {})

    def post(self):
        pass


class CreateOrder(View):
    def get(self, request):
        order_form = OrderForm()

        return render(request, 'Store/create_order.html', {'order_form':order_form})
    
    def post(self, reqeust):
        pass


@csrf_exempt
def add_to_cart(request):
    
    data = json.loads(request.body)
    
    print(data)
    book_id = data['id']
    book_type = data['type']
    book = get_object_or_404(Book, pk=book_id)

    try:
        price = getattr(book, book_type).price
    except AttributeError:
        return JsonResponse({"status":"error"})

    if(book):
        cart = Cart(request)
        cart.add_item(book_id, book_type, str(price))
        return JsonResponse({"status": "ok"})

    return JsonResponse({"status":"error"})


class CategoriesIndex(View):

    def get(self, request, pk):
        # category = Category.objects.filter(slug=category_slug)
        category = get_object_or_404(Category, pk=pk)
        books = category.books.all()
        paginator = Paginator(books, 12)
        page = request.GET.get('page')
        books_page = paginator.get_page(page)
        return render(request, 'Store/category_index.html', {'category':category, 'books':books_page})


class TagsIndex(View):

    def get(self, request):
        tags = request.GET.getlist('tag')
        tags = Tag.objects.filter(text__in=tags)
        books_page = []
        if(tags):
            books = Book.objects.filter(tags__in=tags)
            paginator = Paginator(books, 12)
            page = request.GET.get('page')
            books_page = paginator.get_page(page)
        return render(request, 'Store/tags.html', {"books":books_page})