from django.shortcuts import render
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup
from .models import Account

def update_currency():
    html_content = requests.get("https://www.dolarhoy.co").text
    soup = BeautifulSoup(html_content,"html.parser")
    header_element = soup.select('tr')[17].select('td')[-1].text[2:7]
    DOLLAR = int(header_element.replace(',', ''))
    for account in Account.objects.all():
        if account.currency_dollars:
            account.total_pesos = account.total_dollars * DOLLAR
        else:
            account.total_dollars = round(total_pesos / DOLLAR, 2)
    return DOLLAR

# Create your views here.
def home(request):
    return HttpResponse(update_currency())