from django.shortcuts import render
from django.http import HttpResponse

from .models import Aliment, Reteta, Plan, Cumparaturi

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

def lista_retete(request):
    retete = Reteta.objects.all()
    retete_format = [
        f"<li>{reteta.nume} - {reteta.aliment}</li>"
        for reteta in retete
    ]
    response_string = "<ol>"
    response_string += "".join(retete_format)
    response_string = "</ol>"
    return HttpResponse(f"<ol>{retete_format}</ol>")

def meal_plan(request):
    planuri = Plan.objects.all()
    planuri_format = [
        f"<li>{plan.reteta} - {plan.calorii} - {plan.ziua}</li>"
        for plan in planuri
    ]
    response_string = "<ol>"
    response_string += "".join(planuri_format)
    response_string = "</ol>"
    return HttpResponse(f"<ol>{planuri_format}</ol>")

def lista_cumparaturi(request):
    cumparaturi = Cumparaturi.objects.all()
    cumparaturi_format = [
        f"<li>{necesar.aliment} - {necesar.cantitate}</li>"
        for necesar in cumparaturi
    ]
    response_string = "<ol>"
    response_string += "".join(cumparaturi_format)
    response_string = "</ol>"
    return HttpResponse(f"<ol>{cumparaturi_format}</ol>")