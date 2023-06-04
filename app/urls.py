"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from shop_app.views import *

urlpatterns = [
    path('', HomePageView.as_view(), name="home-page"),
    path('login/', LoginView.as_view(), name="login-page"),
    path('register/', RegisterView.as_view(), name="register-page"),
    path('profile/', UserProfileView.as_view(), name="user-profile"),
    path('change-passwd/', ChangePasswordView.as_view(), name="change-passwd"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('offers/', OffersView.as_view(), name="offers"),
    path('cart/', CartView.as_view(), name="cart"),
    path('clean/', ClearCartView.as_view(), name="clean-cart"),
    path('product/<int:id>/', ProductDetailsView.as_view(), name="product-details")
]
