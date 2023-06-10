from django.shortcuts import render, redirect
from django.http import request, HttpResponse
from django.views import View
from .forms import *
from .models import *
import random
import string
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

cart_number = 1

def array_merge(first_array, second_array):
    """Łączenie dwóch struktur danych w jedną"""
    if isinstance(first_array, list) and isinstance(second_array, list):
        return first_array + second_array
    elif isinstance(first_array, dict) and isinstance(second_array, dict):
        return dict(list(first_array.items()) + list(second_array.items()))
    elif isinstance(first_array, set) and isinstance(second_array, set):
        return first_array.union(second_array)
    return False

class HomePageView(View):
    """Strona główna"""
    def get(self, request):
        """Wyświetlenie strony głównej"""
        return render(request, 'home.html')


class LoginView(View):
    """Logowanie do aplikacji"""
    def get(self, request):
        """Wyświetlenie formularza logowania"""
        form = LoginForm()
        return render(request, 'forms.html', {'form': form, 'title': 'Logowanie'})

    def post(self, request):
        """Weryfikacja danych logowania i logowanie"""
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
    """Fomularz rejestracji na aplikacji"""
    form_class = RegisterForm
    success_url = reverse_lazy('login-page')
    template_name = 'register.html'

    def form_valid(self, form):
        """Tworzenie użytkownika"""
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
    """Wylogowanie użytkownika z aplikacji"""
    def get(self, request):
        logout(request)
        return redirect('home-page')


class UserProfileView(LoginRequiredMixin, View):
    """Wyśiwtlenie profilu użytkownika"""
    def get(self, request):
        """Wyśiwtlenie danych użytkownika na stronie"""
        data = Customer.objects.get(account=request.user)
        return render(request, 'profile.html', {'data': data})


class ChangePasswordView(LoginRequiredMixin, View):
    """Zmiana hasła użytkownika"""
    def get(self, request):
        """Wyświetlenie formularza zmiany hasła"""
        form = ChangePasswordForm()
        return render(request, 'change-passwd.html', {'form': form})

    def post(self, request):
        """Weryfikacja i zmiana hasła"""
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['new_password'] != form.cleaned_data['repeat_new_password']:
                return render(request, 'change-passwd.html', {'form': form, 'info': 'Te hasła nie są takie same!'})
            request.user.set_password(form.cleaned_data['new_password'])
            request.user.save()
            return redirect('user-profile')


class OffersView(View):
    """Wyświetlanie asortymentu sklepu"""
    def get(self, request):
        """Wyświetlanie wszystkich produktów"""
        products = Product.objects.all()
        categories = Category.objects.all()
        return render(request, 'offers.html', {'products': products, 'categories': categories})

    def post(self, request):
        """Wyświtlanie przefiltrowanych produktów"""
        categories = Category.objects.all()
        phrase = request.POST.get('phrase')
        search_categories = request.POST.getlist('search_category')
        min_price = request.POST.get('price_min')
        max_price = request.POST.get('price_max')
        products = Product.objects.all()
        if len(search_categories) != 0:
            products = products.filter(categories__in=search_categories)
        if phrase != '':
            products = products.filter(name__icontains=phrase)
        products = products.filter(price__gte=min_price, price__lte=max_price)
        return render(request, 'offers.html', {'products': products, 'categories': categories})


class ProductDetailsView(View):
    """Wyświetlanie szczegółów produktu"""
    def get(self, request, id):
        """Wyświtlanie zawartości produktu"""
        product = Product.objects.get(id=id)
        return render(request, 'product-details.html', {'product': product})

    def post(self, request, id):
        """Dodawanie produktu do koszyka"""
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
    """Koszyk z asortymentem"""
    def get(self, request):
        """Wyświetl zawartość koszyka"""
        info = request.session.get('cart_item')
        return render(request, 'cart.html', {'info': info, 'price': request.session.get('all_total_price'), 'title': 'Koszyk'})


class ClearCartView(View):
    """Czyszczenie koszyka z zawartości"""
    def get(self, request):
        """Usuń wszystkie produkty z koszyka"""
        global cart_number
        cart_number = 1
        request.session.pop('cart_item', default=None)
        request.session.pop('all_total_price', default=None)
        return redirect('cart')


class DeleteCartProductView(View):
    """Usuwanie konkretnych produktów z koszyka"""
    def get(self, request, id):
        """Usuń wybrany produkt z koszyka"""
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
    """Składanie zamówienia na produkty z koszyka"""
    def get(self, request):
        """Tworzenie zamówienia i wysyłanie maila z potwierdzeniem zamówienia"""
        global cart_number
        characters = string.ascii_letters + string.digits
        code = ''.join(random.choice(characters) for i in range(10))
        cart_item = request.session['cart_item']
        customer = Customer.objects.get(account=request.user)
        sender_email = 'jkosakowski602@gmail.com'
        password = 'mzlskaagjaadqojt'
        subject = f"Zamówienie nr. {code}"
        message = f"""Witaj, {request.user.first_name} {request.user.last_name}, Twoje zamówienie o kodzie
                {code} jest w trakcie realizacji!\n
                Twoje zamówienie:\nNazwa produktu  |  Ilość  |  Cena za sztuke  |  Cena całkowita  |\n\n"""
        order = Order.objects.create(code=code, order_owner=customer, total_price=request.session['all_total_price'])
        for key, value in cart_item.items():
            product = Product.objects.get(id=value['id'])
            product.available -= value['quantity']
            product.save()
            OrderDetails.objects.create(
                product=product,
                order=order,
                quantity=value['quantity'],
                price_per_unit=value['price'],
                total_price=value['total_price'])
            message += f"""{value['name']}  |  {value['quantity']}  |  {value['price']}  |  {value['total_price']}"""
        message += f"""\nCałkowita kwota Twojego zamówienia to {format(request.session['all_total_price'])} złotych."""
        cart_number = 1
        request.session.pop('cart_item', None)
        request.session.pop('all_total_price', None)

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = request.user.email
        msg['Subject'] = subject

        msg.attach(MIMEText(message, 'plain'))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        server.login(sender_email, password)

        text = msg.as_string()
        server.sendmail(sender_email, request.user.email, text)

        server.quit()

        return redirect('home-page')