from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=250)

class Spent(models.Model):
    value = models.FloatField()
    name = models.CharField(max_length=250)