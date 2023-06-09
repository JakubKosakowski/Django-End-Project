import pytest
from django.test import TestCase, Client
from shop_app.models import *
from django.urls import reverse
from django.contrib import auth


class ViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(name='Test product',
                                              description='Description of test product',
                                              price=10.50)

    def test_home_page_get(self):
        response = self.client.get(reverse('home-page'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

        self.product.delete()

    def test_login_get(self):
        response = self.client.get(reverse('login-page'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forms.html')
        self.product.delete()

    def test_login_post(self): # Poprawić
        response = self.client.post(reverse('login-page'),
                                    {'login': 'ELKOSAKO',
                                     'password': 'Boris123!@#'})
        session = self.client.session
        self.assertEqual(response.status_code, 200)
        self.assertIn('_auth_user_id', session)
        self.product.delete()

    def test_register_get(self):
        response = self.client.get(reverse('register-page'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.product.delete()

    def test_register_post(self):
        response = self.client.post(reverse('register-page'),
                                    {'first_name': "AAA",
                                     'last_name': "BBB",
                                     'username': "ASDASD",
                                     'password': "123123",
                                     "password_rep": "123123",
                                     "email": "asdasd@gmail.com",
                                     "street": "AAA",
                                     "postal_code": "12345",
                                     "city": "ASDASD",
                                     "country": "QWERTY"})
        self.assertEqual(response.status_code, 302)
        self.product.delete()

    def test_product_details_get(self):
        response = self.client.get(reverse('product-details', args=[self.product.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product-details.html')
        self.product.delete()

    def test_product_details_post(self):
        response = self.client.post(reverse('product-details', args=[self.product.id]),
                                    {'amount-number': 2})
        session = self.client.session
        self.assertEqual(response.status_code, 302)
        self.assertEqual(session['all_total_price'], 21.00)
        self.assertIn('cart_item', session)
        self.product.delete()

    def test_cart_get(self):
        response = self.client.get(reverse('cart'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart.html')
        self.product.delete()

    def test_clear_cart_get(self):
        response = self.client.get(reverse('clean-cart'))

        self.assertEqual(response.status_code, 302)
        self.product.delete()

    def test_order_get(self): # Popraw
        response = self.client.get(reverse('order'))

        session = self.client.session
        self.assertEqual(response.status_code, 302)
        self.assertIn('all_total_price', session)
        self.product.delete()

