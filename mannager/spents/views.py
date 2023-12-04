from django.shortcuts import render
from django.http import HttpResponse
import requests
import json
from bs4 import BeautifulSoup
from django.views.decorators.csrf import csrf_exempt
from .models import Account, Spent, Earn, SpentCategory, EarnCategory, SubCash
import datetime


def update_currency():
    html_content = requests.get("https://www.dolarhoy.co").text
    soup = BeautifulSoup(html_content,"html.parser")
    header_element = soup.select('tr')[17].select('td')[-1].text[2:7]
    DOLLAR = int(header_element.replace(',', ''))
    for account in Account.objects.all():
        if account.currency_dollars:
            account.total_pesos = round(account.total_dollars * DOLLAR, 0)
        else:
            account.total_dollars = round(account.total_pesos / DOLLAR, 2)
        account.save()
    return DOLLAR

def pesos_dollar(pesos):
    dollar = update_currency()
    return round(pesos / dollar, 2)

def dollar_pesos(dollar):
    valor_dollar = update_currency()
    return round(dollar * valor_dollar, 0)

def add_account(id, pesos, dollar):
    account = Account.objects.get(id=id)
    if account.currency_dollars:
        account.total_dollars += dollar
    else:
        account.total_pesos += pesos
    account.save()
    update_currency()

def rest_account(id, pesos, dollar):
    account = Account.objects.get(id=id)
    if account.currency_dollars:
        account.total_dollars -= dollar
    else:
        account.total_pesos -= pesos
    account.save()
    update_currency()

def subcash_spent(account_id, dollar):
    sub_cashes = SubCash.objects.filter(account=Account.objects.get(id=account_id)).order_by('buy_at')
    index = 0
    while dollar > 0:
        sub_cash = sub_cashes[index]
        relative = sub_cash.dollars - dollar 
        if relative > 0:
            sub_cash.dollars -= dollar
            sub_cash.save()
            dollar = 0
        else:
            sub_cash.delete()
            dollar = relative * -1


# Create your views here.
def home(request):
    dollar = update_currency()
    return render(request, 'main.html', {'dollar' : dollar})

@csrf_exempt
def delete(request): 
    if request.method == "POST":
        data = json.loads(request.body)
        if data['type'] == 0:
            obj = Earn.objects.filter(id=data['id'])
            rest_account(obj.account.id, obj.pesos, obj.dollars)
            if obj.in_cash and obj.in_dollar:
                subcash_spent(obj.account.id, obj.dollars) #Falta perfeccionar este elemento 
                                                           # Pq quita dollares baratos y no los comprados
        else:
            obj = Spent.objects.filter(id=data['id'])
            add_account(obj.account.id, obj.pesos, obj.dollars)

            if obj.in_cash and obj.in_dollar:
                SubCash.objects.create(dollars=obj.dollars, account=obj.account,
                but_at=round(obj.pesos / obj.dollars, 0), earn=None)

        obj.delete()
        return HttpResponse(status=202)
    return HttpResponse(status=400)

@csrf_exempt
def add(request):
    if request.method == "POST":
        data = json.loads(request.body)
        if data['in_dollar']:
            dollars = data['value']
            pesos = dollar_pesos(dollars)
        else:
            pesos = data['value']
            dollars = pesos_dollar(pesos)

        if data ['type'] == 0:
            account = Account.objects.get(id=data['account'])
            new_earn = Earn.objects.create(
                dollars=dollars,
                pesos=pesos,
                name=data['name'],
                date=datetime.datetime.now(),
                category=EarnCategory.objects.get(id=data['category']),
                account=account,
                in_dollar=data['in_dollar'],
                in_cash=data['in_cash']
            )
            add_account(data['account'], pesos, dollars)
            
            if data['in_cash'] and data['in_dollar']:
                SubCash.objects.create(dollars=dollars, buy_at=update_currency(), account=account, earn=new_earn)

        else:
            Spent.objects.create(
                dollars=dollars,
                pesos=pesos,
                name=data['name'],
                date=datetime.datetime.now(),
                category=SpentCategory.objects.get(id=data['category']),
                account=Account.objects.get(id=data['account']),
                in_dollar=data['in_dollar'],
                in_cash=data['in_cash']
            )
            rest_account(data['account'], pesos, dollars)

            if data['in_cash'] and data['in_dollar']:
                subcash_spent(data['account'], dollars)
            
        return HttpResponse(status=200)
    
# @csrf_exempt 
# def edit(request):
    # if request.method == "POST":
        # data = json.loads(request.body)
        # if data['type'] == 0:
            # 