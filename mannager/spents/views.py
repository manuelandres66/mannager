from django.shortcuts import render
from django.http import HttpResponse
import requests

# Create your views here.
def home(request):
    headers =  {'X-RapidAPI-Key': '3b9b9c776emsh06c4f835f217b1ep1daf80jsn05841d6a2883',
                'X-RapidAPI-Host': 'currency-exchange.p.rapidapi.com'}
    dollar = requests.get("https://currency-exchange.p.rapidapi.com/listquotes", headers=headers)
    print(dollar)
    return HttpResponse(dollar)