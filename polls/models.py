
from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)


class Product(models.Model):
    title = models.CharField(max_length=30)
    Owner = models.CharField(max_length=30)


class Lesson(models.Model):
    title = models.CharField(max_length=30)
    product_belong = models.CharField(max_length=30)
# Create your models here.
