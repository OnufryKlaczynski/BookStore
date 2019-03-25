from django.shortcuts import render
from django.views import View
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import SignUpForm, OrderDataForm



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
        orders = user.orders

        return render(request, 'Account/order_history.html', {'orders':orders})