from django.db import models


class Product(models.Model):
    name = models.CharField()
    description = models.TextField()
    available = models.IntegerField(default=100)