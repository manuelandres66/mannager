from django.shortcuts import render
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup
from .models import Account, Spent, Earn

def update_currency():
    html_content = requests.get("https://www.dolarhoy.co").text
    soup = BeautifulSoup(html_content,"html.parser")
    header_element = soup.select('tr')[17].select('td')[-1].text[2:7]
    DOLLAR = int(header_element.replace(',', ''))
    for account in Account.objects.all():
        if account.currency_dollars:
            account.total_pesos = account.total_dollars * DOLLAR
        else:
            account.total_dollars = round(account.total_pesos / DOLLAR, 2)
        account.save()
    return DOLLAR

# Create your views here.
def home(request):
    dollar = update_currency()
    return render(request, 'main.html', {'dollar' : dollar})

def delete(request):
    if request.method == "POST":
        if request.POST['type'] == 0:
            Earn.objects.filter(id=request.POST['id']).delete()
        elif request.POST['type'] == 1:
            Spent.objects.filter(id=request.POST['id']).delete()
        return HttpResponse(status=202)
    return HttpResponse(status=400)