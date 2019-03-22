from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, reverse
from django.http.response import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

import json
import urllib

from .models import Book, Author, Reader, Category, Tag, Order
from .cart import CART, Cart
from .forms import OrderForm, DotPayForm




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


class CreateOrder(View):
    def get(self, request):
        # order_id = request.session.get('order', None)
        # if order_id:
        #     try:
        #         order = Order.objects.get(pk=order_id)
        #         # order_form = OrderForm(instance=order)
        #     except Order.DoesNotExist:
        #         pass
        order_form = OrderForm()
        return render(request, 'Store/create_order.html', {'order_form':order_form})
    
    def post(self, request):
        
        order_form = OrderForm(request.POST)
        print(order_form.errors)
        if order_form.is_valid():
            order = order_form.save()
            cart = Cart(request)
            items = cart.create_order_items(order)
            order.items.set(items)
            
            request.session['order'] = order.pk
            
            return redirect(reverse('Store:order_confirmation'))
        
        return render(request, 'Store/create_order.html', {'order_form':order_form})


class OrderConfirmation(View):
    
    def get(self, reqeust):
        amount = "10.00"
        currency = "PLN"
        description = "nie wiem"
        urlc = urllib.parse.urljoin("http://127.0.0.1:8000", reverse('Store:success'))
        url = ''
        channel = 1
        firstname = 'asdfasdf'
        lastname = 'asdfasf'
        email = 'asd@wp.pl'
        data_for_dot_pay = {
            'api_version':'dev',
            'id':790190,
            'amount': amount,
            'current': currency,
            'description' : description,
            
            'channel': channel,
            'firstname':firstname,
            'lastname':lastname,
            'email':email,
            'type': 4,
            'URL': urlc,
            'URLC': urlc,
            'bylaw':1 ,
            'personal_data': 1,
        }
        dotpay_form = DotPayForm(initial=data_for_dot_pay)
        order_pk = reqeust.session.get('order')
        order = get_object_or_404(Order, pk=order_pk)
        items = order.items.all()
        if(order):
            return render(
                reqeust,
                 'Store/order_confirmation_and_payment_method.html',
                  {
                      "order":order,
                      "items":items, 
                      "dotpay_form":dotpay_form,
                      "url":"https://ssl.dotpay.pl/test_payment/"
                  })
        

  
class DidSucces(View):

    def get(self, request):
        status_choices = ("new", "completed", "rejected")
        did_succes = request.GET.get("status")

        return HttpResponse("Ok")


def dotpay_server_confirmation(request):
    request.GET.get('id')
    request.GET.get('operation_number')
    request.GET.get('operation_type')
    request.GET.get('operation_status')
    request.GET.get('operation_amount')
    request.GET.get('operation_currency')
    request.GET.get('is_completed')
    request.GET.get('operation_original_amount')
    request.GET.get('operation_original_currency')
    request.GET.get('operation_datetime')
    request.GET.get('operation_related_number')
    request.GET.get('control')
    request.GET.get('description')
    request.GET.get('email')
    request.GET.get('control')

    return HttpResponse("OK")



class ChooseAccountMethod(View):
    def get(self, request):
        if request.user.is_authenticated:
            pass

        return render(request, 'Store/choose_account_method.html', {})

    def post(self):
        pass

