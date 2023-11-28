from django.shortcuts import render
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup

def update_currency():
    html_content = requests.get("https://www.dolarhoy.co").text
    soup = BeautifulSoup(html_content,"html.parser")
    header_element = soup.select('tr')[17].select('td')[-1].text[2:7]
    DOLLAR = int(header_element.replace(',', ''))
    return DOLLAR

# Create your views here.
def home(request):
    return HttpResponse(update_currency())