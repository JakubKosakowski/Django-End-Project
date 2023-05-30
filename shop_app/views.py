from django.shortcuts import render, redirect
from django.http import request
from django.views import View
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


class HomePageView(View):
    def get(self, request):
        return render(request, 'home.html')


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['login']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home-page')
            return render(request, 'login.html', {'form': form, 'info': 'Zły login lub hasło!'})