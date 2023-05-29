from django.shortcuts import render
from django.http import request
from django.views import View


class HomePageView(View):
    def get(self, request):
        return render(request, 'home.html')
