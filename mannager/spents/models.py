from django.db import models

# Create your models here.

class Account(models.Model):
    name = models.CharField(max_length=250)
    total_dollars = models.FloatField()
    total_pesos = models.IntegerField()
    currency_dollars = models.BooleanField()
    def __str__(self):
        return f"{self.name}({self.id})"

class SubCash(models.Model):
    dollars = models.FloatField()
    buy_at = models.IntegerField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    earn = models.ForeignKey('Earn', on_delete=models.CASCADE)

class SpentCategory(models.Model):
    name = models.CharField(max_length=250)
    def __str__(self):
        return f"{self.name}({self.id})"

class Spent(models.Model):
    dollars = models.FloatField()
    pesos = models.IntegerField()
    name = models.CharField(max_length=250)
    date = models.DateTimeField()
    category = models.ForeignKey(SpentCategory, on_delete=models.RESTRICT)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    in_dollar = models.BooleanField()

class EarnCategory(models.Model):
    name = models.CharField(max_length=250)
    def __str__(self):
        return f"{self.name}({self.id})"

class Earn(models.Model):
    dollars = models.FloatField()
    pesos = models.IntegerField()
    name = models.CharField(max_length=250, null=True, blank=True)
    date = models.DateTimeField()
    category = models.ForeignKey(EarnCategory, on_delete=models.RESTRICT)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)
    in_dollar = models.BooleanField()