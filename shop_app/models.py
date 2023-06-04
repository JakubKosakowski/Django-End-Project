from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()


class Product(models.Model):
    name = models.CharField()
    description = models.TextField()
    available = models.IntegerField(default=100)
    price = models.DecimalField(null=True, max_digits=6, decimal_places=2)
    categories = models.ManyToManyField(Category)


class Customer(models.Model):
    account = models.ForeignKey(User, on_delete=models.CASCADE)
    street = models.CharField(max_length=60)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=60)
    country = models.CharField(max_length=50)


class Order(models.Model):
    code = models.CharField(max_length=10, unique=True)
    order_date = models.DateField(default=date.today())
    order_owner = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderDetails')


class OrderDetails(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    price_per_unit = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.IntegerField()
