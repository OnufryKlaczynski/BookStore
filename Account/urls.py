
from django.contrib import admin
from django.urls import path
from django.urls import include

from .views import  SignUp, AccountOptions

app_name = 'Account'

urlpatterns = [
       path("", AccountOptions.as_view(), name="account_options" ),
       path("signup/", SignUp.as_view(), name="sign_up" ),
]
