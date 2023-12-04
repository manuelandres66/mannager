from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests
import json
from bs4 import BeautifulSoup
from django.views.decorators.csrf import csrf_exempt
from .models import Account, Spent, Earn, SpentCategory, EarnCategory, SubCash
from django.utils import timezone
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



# Create your views here.

@csrf_exempt
def delete(request): 
    if request.method == "POST":
        data = json.loads(request.body)
        if data['type'] == 0:
            obj = Earn.objects.filter(id=data['id'])
            rest_account(obj.account.id, obj.pesos, obj.dollars)
            if obj.in_cash and obj.in_dollar:
                subcash_spent(obj.account.id, obj.dollars) #ERROR A
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
                date=timezone.now(),
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
                date=timezone.now(),
                category=SpentCategory.objects.get(id=data['category']),
                account=Account.objects.get(id=data['account']),
                in_dollar=data['in_dollar'],
                in_cash=data['in_cash']
            )
            rest_account(data['account'], pesos, dollars)

            if data['in_cash'] and data['in_dollar']:
                subcash_spent(data['account'], dollars)
            
        return HttpResponse(status=200)
    
@csrf_exempt 
def edit(request):
    if request.method == "POST":
        data = json.loads(request.body)
        earn = data['type'] == 0
        obj = Earn.objects.get(id=data['id']) if earn else Spent.objects.get(id=data['id'])
        ac, pe, dol, in_cash = data['account'], data['pesos'], data['dollars'],data['in_cash']
        ac_obj = Account.object.get(id=ac)

        if obj.account.id != ac: #Changing account
            if in_cash != ac_obj.in_cash: #Check compatibily bewteen account and edit
                return JsonResponse({'error':'Imposible Cash Transference'}, status=500)

            rest_account(obj.account.id, obj.pesos, obj.dollars)
            add_account(ac, pe, dol)

        else:
            difference = dol - obj.dollars #Check if earned or spent some money in the general account
            if difference >= 0:
                add_account(ac, pe, dol) if earn else rest_account(ac, pe, dol)
            else:
                rest_account(ac, pe, dol) if earn else add_account(ac, pe, dol)


        #SubCash Stuff
        if in_cash != obj.in_cash:
            if in_cash: #Changed to cash
                Subcash.objects.create(dollars=dol, buy_at=round(pe/dol,0),earn=obj,account=ac_obj) if earn else subcash_spent(ac, dol) #ERROR A
            else: #Changed to virtual
                Subcash.objects.create(dollars=obj.dollars, buy_at=round(obj.pesos/obj.dollars,0),account=obj.account) if not earn else subcash_spent(obj.account.id, obj.dollars) #ERROR A

        obj.dollars=dol
        obj.pesos=pe
        obj.name=data['name']
        obj.date=data['date']
        obj.category=SpentCategory.objects.get(id=data['category'])
        obj.account=ac_obj
        obj.in_dollar=data['in_dollar']
        obj.in_cash=in_cash
        obj.save()
        return HttpResponse(status=200)
            

@csrf_exempt
def get_earn(request):
    one_day = datetime.datetime.now() - datetime.timedelta(days=1)
    print(one_day)
    one_day_obj = Earn.objects.filter(date__gte=one_day, date__lt=timezone.now())
    print(one_day_obj.values())

def home(request):
    dollar = update_currency()
    get_earn(request)
    return render(request, 'main.html', {'dollar' : dollar})