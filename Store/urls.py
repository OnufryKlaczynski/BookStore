from django.contrib import admin
from django.urls import path
from .views import Index, BookDetail, AuthorIndex, AuthorDetail, DisplayCart  , add_to_cart

app_name =  'Store'
urlpatterns = [
    path("", Index.as_view(), name='index'),
    path("books/<int:pk>", BookDetail.as_view(), name='book_detail'),
    path("authors/", AuthorIndex.as_view(), name='author_index'),
    path("authors/<int:pk>/", AuthorDetail.as_view(), name='author_detail'),
    path("cart/", DisplayCart.as_view(), name='display_cart'),
    path("add_to_cart/", add_to_cart , name='add_to_cart'),

]
