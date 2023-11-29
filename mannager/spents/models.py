from django.db import models

# Create your models here.

class Account(models.Model):
    name = models.CharField(max_length=250)
    total_dollars = models.FloatField()
    total_pesos = models.IntegerField()
    currency_dollars = models.BooleanField()
    def __str__(self):
        return self.name

class SubCash(models.Model):
    dollars = models.FloatField()
    buy_at = models.IntegerField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

class SpentCategory(models.Model):
    name = models.CharField(max_length=250)
    def __str__(self):
        return self.name

class Spent(models.Model):
    dollars = models.FloatField()
    pesos = models.IntegerField()
    name = models.CharField(max_length=250)
    date = models.DateTimeField()
    category = models.ForeignKey(SpentCategory, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

class EarnCategory(models.Model):
    name = models.CharField(max_length=250)
    def __str__(self):
        return self.name

class Earn(models.Model):
    money = models.FloatField()
    pesos = models.IntegerField()
    name = models.CharField(max_length=250, null=True, blank=True)
    date = models.DateTimeField()
    category = models.ForeignKey(EarnCategory, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)