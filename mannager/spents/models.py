from django.db import models

# Create your models here.

class SpentCategory(models.Model):
    name = models.CharField(max_length=250)
    def __str__(self):
        return self.name

class Spent(models.Model):
    money = models.FloatField()
    name = models.CharField(max_length=250)
    category = models.ForeignKey(SpentCategory, on_delete=models.CASCADE, null=True, blank=True)