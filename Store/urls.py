from django.contrib import admin
from django.urls import path


from . import views

app_name =  'Store'

urlpatterns = [
    path("", views.Index.as_view(), name='index'),
    path("books/<int:pk>", views.BookDetail.as_view(), name='book_detail'),
    path("authors/", views.AuthorIndex.as_view(), name='author_index'),
    path("authors/<int:pk>/", views.AuthorDetail.as_view(), name='author_detail'),
    path("cart/",views. DisplayCart.as_view(), name='display_cart'),
    path("account-method/", views.ChooseAccountMethod.as_view() , name='choose_account_method'),
    path("create-order/", views.CreateOrder.as_view() , name='create_order'),
    path("add_to_cart/", views.add_to_cart , name='add_to_cart'),

]
