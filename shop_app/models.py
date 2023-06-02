from django.db import models
from django.contrib.auth.models import User

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
