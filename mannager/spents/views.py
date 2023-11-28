from django.shortcuts import render
from django.http import HttpResponse
import requests

# Create your views here.
def home(request):
    dollar = requests.get("https://api.exchangeratesapi.io/v1/latest?access_key=8a920d3e399466722e755da29ad02a18&base=COP&symbols=USA")
    print(dollar)
    return HttpResponse(dollar)