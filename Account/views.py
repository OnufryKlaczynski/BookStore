from django.shortcuts import render
from django.views import View
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from .forms import SignUpForm, OrderDataForm

from Store.models import Book


class SignUp(View):

    def get(self, request):
        form = SignUpForm()
        return render(request, 'Account/sign_up.html', {'form':form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            
            user = authenticate(email=email, password=password)
            login(request, user)
            return redirect('Store:index')

        else:
            form = SignUpForm()
            return render(request, 'Account/sign_up.html', {'form':form})



class AccountOptions(LoginRequiredMixin,View):
    
    
    def get(self, request):
        user = request.user
        
        order_data_form = OrderDataForm(instance=user)
        
        context = {
            'order_data_form': order_data_form,
            }
        return render(request, 'Account/order_data.html', context)
    

    def post(self, request):
        if request.user.is_authenticated:
            
            order_data_form = OrderDataForm(request.POST, instance=request.user)
        else:
            order_data_form = OrderDataForm(request.POST)
        if order_data_form.is_valid():
            order_data_form.save()

        return render(request, 'Account/order_data.html', {'order_data_form':order_data_form})


class OrderHistory(LoginRequiredMixin, View):

    def get(self, request):
        user = request.user
        orders = user.orders.all()

        return render(request, 'Account/order_history.html', {'orders':orders})


class ObservedBooks(LoginRequiredMixin, View):

    def get(self, request):
        user = request.user
        observed = user.observed.all()

        return render(request, 'Account/observed.html', {'observed':observed})


    def post(self, request, pk):

        user = request.user
        book = get_object_or_404(Book, pk=pk)
        user.observed.add(book)

        return JsonResponse({"status":"ok"})

    def delete(self, request, pk):
        user = request.user
        book = get_object_or_404(Book, pk=pk)
        user.observed.remove(book)
        
        return JsonResponse({"status":"ok"})