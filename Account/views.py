from django.shortcuts import render
from django.views import View
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect


from .forms import SignUpForm

class Index(View):

    def get(self, request):

        return render(request, '', {})



class SignUp(View):

    def get(self, request):
        form = SignUpForm()
        return render(request, 'Account/sign_up.html', {'form':form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if(form.is_valid):
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            login(request, user)
            return redirect('Store:index')

        else:
            form = SignUpForm()
            return render(request, 'Account/sign_up.html', {'form':form})