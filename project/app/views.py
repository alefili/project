from django.shortcuts import render
from django.http import HttpResponse

from .models import Aliment

# Create your views here.
def welcome(request):
    return HttpResponse("welcome")

def lista_alimente(request):
    alimente = Aliment.objects.all()
    alimente_format = [
        f"<li>{aliment.titlu} - {aliment.calorii} - {aliment.stoc}</li>"
        for aliment in alimente
    ]
    response_string = "<ol>"
    response_string += "".join(alimente_format)
    response_string = "</ol>"
    return HttpResponse(f"<ol>{alimente_format}</ol>")