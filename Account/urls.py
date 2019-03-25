
from django.contrib import admin
from django.urls import path
from django.urls import include

from .views import  SignUp, AccountOptions, OrderHistory

app_name = 'Account'

urlpatterns = [
       path("", AccountOptions.as_view(), name="account_options" ),
       path("order-history/", OrderHistory.as_view(), name="order-history" ),
       path("signup/", SignUp.as_view(), name="sign_up" ),
]
