from django.shortcuts import render, redirect
from django.http import request, HttpResponse
from django.views import View
from .forms import *
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin

cart_number = 1

def array_merge(first_array, second_array):
    if isinstance(first_array, list) and isinstance(second_array, list):
        return first_array + second_array
    elif isinstance(first_array, dict) and isinstance(second_array, dict):
        return dict(list(first_array.items()) + list(second_array.items()))
    elif isinstance(first_array, set) and isinstance(second_array, set):
        return first_array.union(second_array)
    return False

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
    template_name = 'register.html'

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


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request):
        data = Customer.objects.get(account=request.user)
        return render(request, 'profile.html', {'data': data})


class ChangePasswordView(LoginRequiredMixin, View):
    def get(self, request):
        form = ChangePasswordForm()
        return render(request, 'change-passwd.html', {'form': form})

    def post(self, request):
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['new_password'] != form.cleaned_data['repeat_new_password']:
                return render(request, 'change-passwd.html', {'form': form, 'info': 'Te hasła nie są takie same!'})
            request.user.set_password(form.cleaned_data['new_password'])
            request.user.save()
            return redirect('user-profile')


class OffersView(View):
    def get(self, request):
        products = Product.objects.all()
        return render(request, 'offers.html', {'products': products})


class ProductDetailsView(View):
    def get(self, request, id):
        product = Product.objects.get(id=id)
        return render(request, 'product-details.html', {'product': product})

    def post(self, request, id):
        global cart_number
        quantity = int(request.POST.get('amount-number'))
        ordered_product = Product.objects.get(id=id)
        product_dict = {
            str(cart_number): {
                'id': int(id),
                'name': ordered_product.name,
                'price': float(ordered_product.price),
                'quantity': quantity,
                'total_price': float(ordered_product.price) * quantity
            }
        }
        all_total_price = 0
        request.session['modified'] = True
        flag = True
        if 'cart_item' in request.session:
            for key, value in request.session['cart_item'].items():
                if id == request.session['cart_item'][key]['id']:
                    old_quantity = request.session['cart_item'][key]['quantity']
                    total_quantity = old_quantity + quantity
                    request.session['cart_item'][key]['quantity'] = total_quantity
                    request.session['cart_item'][key]['total_price'] = round(
                        total_quantity * float(ordered_product.price), 2)
                    flag = False
            if flag:
                request.session['cart_item'] = array_merge(request.session['cart_item'], product_dict)
                cart_number += 1
            for key, value in request.session['cart_item'].items():
                all_total_price += round(request.session['cart_item'][key]['total_price'], 2)
        else:
            request.session['cart_item'] = product_dict
            all_total_price += quantity * float(ordered_product.price)
            cart_number += 1

        request.session['all_total_price'] = all_total_price

        return redirect('cart')


class CartView(View):
    def get(self, request):
        info = request.session.get('cart_item')
        return render(request, 'cart.html', {'info': info, 'price': request.session.get('all_total_price'), 'title': 'Koszyk'})


class ClearCartView(View):
    def get(self, request):
        global cart_number
        cart_number = 1
        request.session.pop('cart_item', default=None)
        request.session.pop('all_total_price', default=None)
        return redirect('cart')


class DeleteCartProductView(View):
    def get(self, request, id):
        global cart_number
        all_total_price = 0
        for item in request.session['cart_item'].items():
            if int(item[0]) == id:
                request.session['cart_item'].pop(item[0], None)
                if 'cart_item' in request.session:
                    for key, value in request.session['cart_item'].items():
                        all_total_price += int(request.session['cart_item'][key]['total_price'])
                break
        if all_total_price == 0:
            request.session.clear()
        else:
            request.session['all_total_price'] = round(all_total_price, 2)

        cart_number -= 1
        return redirect('cart')


class OrderView(View):
    def get(self, request):
        return HttpResponse("<h1>Order site</h1>")