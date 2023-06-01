from django.shortcuts import render, redirect
from django.http import request
from django.views import View
from .forms import *
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import FormView


class HomePageView(View):
    def get(self, request):
        return render(request, 'home.html')


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'forms.html', {'form': form, 'title': 'Logowanie'})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['login']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home-page')
            return render(request, 'forms.html', {'form': form, 'title': 'Logowanie', 'info': 'Zły login lub hasło!'})


class RegisterView(FormView):
    form_class = RegisterForm
    success_url = reverse_lazy('login-page')
    template_name = 'forms.html'

    def form_valid(self, form):
        user = User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'],
                                        form.cleaned_data['password'])
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.save()
        Customer.objects.create(account=user,
                                street=form.cleaned_data['street'],
                                postal_code=form.cleaned_data['postal_code'],
                                city=form.cleaned_data['city'],
                                country=form.cleaned_data['country'])
        return super().form_valid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home-page')