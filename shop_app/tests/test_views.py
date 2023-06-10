import pytest
from django.test import TestCase, Client
from shop_app.models import *
from shop_app.forms import *
from django.urls import reverse
from django.contrib import auth


class ViewsTests(TestCase):
    """Testy widoków aplikacji shop_app"""
    def setUp(self):
        """Ustawianie testowanych wartości"""
        self.client = Client()
        self.user = User.objects.create_user(username="admin", password="admin", email="asdasd@gmail.com", first_name="AAA", last_name="BBB")
        self.customer = Customer.objects.create(account=self.user,
                                                street="AAA",
                                                postal_code="213721",
                                                city="ASDASD",
                                                country="QWERTY")
        self.category = Category.objects.create(name="Test category",
                                                description="Description of test product")
        self.product = Product.objects.create(name='Test product',
                                              description='Description of test product',
                                              price=10.50)
        self.products = [Product.objects.create(
            name=f'Product {i}',
            description=f'Description of {i}',
            price=10+i
        ) for i in range(10)]
        self.product.categories.add(self.category)
        self.product.save()

    def test_home_page_get(self):
        """Test wyświtlanie strony głównej"""
        response = self.client.get(reverse('home-page'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

        self.product.delete()

    def test_login_get(self):
        """Test wyświetlania strony do logowania"""
        response = self.client.get(reverse('login-page'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forms.html')
        self.product.delete()

    def test_login_post(self):
        """Test wyświetlania strony po prawidłowym logowaniu"""
        form = LoginForm(data={'login': self.user.username, 'password': self.user.password})
        self.assertTrue(form.is_valid())

    def test_register_get(self):
        """Test wyświetlania strony do rejestracji"""
        response = self.client.get(reverse('register-page'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.product.delete()

    def test_register_post(self):
        """Test wyświetlania strony po prawidłowej rejestracji"""
        form = RegisterForm(data={"first_name": "ADC",
                              "last_name": "QWEASD",
                              "username": "POWER",
                              "password": "GHJFHJ",
                              "password_rep": "GHJFHJ",
                              "email": "ADCQWEASD@gmail.com",
                              "street": "LKSNO",
                              "postal_code": "12345",
                              "city": "ASDASD",
                              "country": "QWERTY"})

        self.assertTrue(form.is_valid())

    def test_logout_get(self):
        """Test opcji wylogowania z aplikacji"""
        self.client.force_login(user=self.user)
        response = self.client.get(reverse('logout'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_user_profile_get(self):
        """Test wyświetlania zawartości profilu użytkownika"""
        self.client.force_login(user=self.user)
        response = self.client.get(reverse('user-profile'))

        self.assertEqual(response.status_code, 200)

    def test_change_password_get(self):
        """Test wyświetlania formularza zmiany hasła"""
        self.client.force_login(user=self.user)
        response = self.client.get(reverse('change-passwd'))

        self.assertEqual(response.status_code, 200)

    def test_change_password_post(self):
        """Test działania aplikacji po prawidłowej zmianie hasła"""
        self.client.force_login(user=self.user)
        response = self.client.post(reverse('change-passwd'), {'new_password': "ASDASD", "repeat_new_password": "ASDASD"})

        self.assertEqual(response.status_code, 302)

    def test_offers_get(self):
        """Test wyświetlania strony z produktami"""
        response = self.client.get(reverse('offers'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'offers.html')
        self.assertEqual(len(response.context['products']), 11)

    def test_product_details_get(self):
        """Test wyświetlania szczegółowych danych produktu"""
        response = self.client.get(reverse('product-details', args=[self.product.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product-details.html')
        self.product.delete()

    def test_product_details_post(self):
        """Test dodawania produktu do koszyka"""
        response = self.client.post(reverse('product-details', args=[self.product.id]),
                                    {'amount-number': 2})
        session = self.client.session
        self.assertEqual(response.status_code, 302)
        self.assertEqual(session['all_total_price'], 21.00)
        self.assertIn('cart_item', session)
        self.product.delete()

    def test_cart_get(self):
        """Test wyświtlania zawartości koszyka"""
        response = self.client.get(reverse('cart'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart.html')
        self.product.delete()

    def test_clear_cart_get(self):
        """Test usuwania wszystkich produktów z koszyka"""
        response = self.client.get(reverse('clean-cart'))

        self.assertEqual(response.status_code, 302)
        self.product.delete()

    def test_delete_product_get(self):
        """Test usuwania konkretnego produktu z koszyka"""
        session = self.client.session
        session['cart_item'] = {"1": {
            'id': self.product.id,
            'name': self.product.name,
            'price': self.product.price,
            'quantity': 2,
            'total_price': float(self.products[0].price) * 2
        }}
        session.save()
        response = self.client.get(reverse('delete', args=[self.product.id]))

        self.assertEqual(len(session['cart_item']), 1)
        self.assertEqual(response.status_code, 302)

    def test_order_get(self):
        """Test składania zamówienia na produkty z koszyka"""
        self.client.force_login(user=self.user)
        self.product.id = 4
        self.product.save()
        session = self.client.session
        session['cart_item'] = {"1": {
            'id': self.product.id,
            'name': self.product.name,
            'price': self.product.price,
            'quantity': 2,
            'total_price': float(self.product.price) * 2
        }}
        session['all_total_price'] = float(self.product.price) * 2
        session.save()

        response = self.client.get(reverse('order'))
        self.assertEqual(response.status_code, 302)
        self.product.delete()

