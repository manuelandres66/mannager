from django.db import models

# Create your models here.

class Account(models.Model):
    name = models.CharField(max_length=250)
    total = models.FloatField()

class SpentCategory(models.Model):
    name = models.CharField(max_length=250)
    def __str__(self):
        return self.name

class Spent(models.Model):
    money = models.FloatField()
    name = models.CharField(max_length=250, null=True, blank=True)
    date = models.DateTimeField()
    category = models.ForeignKey(SpentCategory, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)

class EarnCategory(models.Model):
    name = models.CharField(max_length=250)
    def __str__(self):
        return self.name

class Earn(models.Model):
    money = models.FloatField()
    name = models.CharField(max_length=250, null=True, blank=True)
    date = models.DateTimeField()
    category = models.ForeignKey(EarnCategory, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)