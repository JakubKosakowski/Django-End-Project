from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()


class Product(models.Model):
    name = models.CharField()
    description = models.TextField()
    available = models.IntegerField(default=100)
    categories = models.ManyToManyField(Category)
