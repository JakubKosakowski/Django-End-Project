from django.shortcuts import render
from django.http import request
from django.views import View
from .forms import *


class HomePageView(View):
    def get(self, request):
        return render(request, 'home.html')


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})