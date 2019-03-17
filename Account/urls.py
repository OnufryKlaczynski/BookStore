
from django.contrib import admin
from django.urls import path
from django.urls import include

from .views import Index, SignUp

app_name = 'Account'

urlpatterns = [
       path("signup/", SignUp.as_view(), name="sign_up" ),
]
