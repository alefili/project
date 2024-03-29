from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy

from .forms import *
from .decorators import is_staff
from .models import Aliment, Reteta, Plan, Cumparaturi

from django.db.models import F

# Create your views here.
def welcome(request):
    retete = Reteta.objects.all()[:3]
    return render(request, "index.html", {"retete": retete})

def lista_alimente(request):
    alimente = Aliment.objects.all()
    alimente = alimente.order_by("titlu") 
    return render(request, "alimente.html", {"alimente": alimente})

def aliment(request, id):
    try:
        aliment = Aliment.objects.get(id=id)
    except Aliment.DoesNotExist:
        return HttpResponse("404")
    return render(request, "aliment.html", {"aliment": aliment})

def lista_retete(request):
    retete = Reteta.objects.all()
    retete = retete.order_by("nume") 
    return render(request, "retete.html", {"retete": retete})

def reteta(request, id):
    try:
        reteta = Reteta.objects.get(id=id)
    except Reteta.DoesNotExist:
        return HttpResponse("404")
    return render(request, "reteta.html", {"reteta": reteta})

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

def contact(request):
    form = ContactForm()
    mesaj = ""
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            subiect = form.cleaned_data["subiect"]
            mesaj = form.cleaned_data["mesaj"]
            email = form.cleaned_data["email"]
            copie = form.cleaned_data["trimite_copie"]
            copie_text = f"{type(copie)}, {copie}"
            print(type(copie), copie)
            send_mail(subiect, mesaj+copie_text, from_email="contact@siit.ro", recipient_list=[email])
            #return redirect("/")
    return render(request, "contact.html", {"form": form, "mesaj": mesaj})

def custom_login(request):
    form = CustomLoginForm()
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            login(request, form.authenticate_user)
            return redirect("/")

    return render(request, 'login.html', {'form': form})



def logout_view(request):
    logout(request)
    return redirect("/")

@is_staff
@login_required
def adauga_aliment(request):
    formular = AlimentForm()
    if request.method == "POST":
        formular = AlimentForm(request.POST)
        if formular.is_valid():
            formular.save()
            return redirect(reverse("pagina-aliment"))
    return render(request, "adauga_aliment.html", {"form": formular})

@is_staff
@login_required
def adauga_reteta(request):
    formular = RetetaForm()
    if request.method == "POST":
        formular = RetetaForm(request.POST)
        if formular.is_valid():
            formular.save()
            return redirect(reverse("pagina-reteta"))
    return render(request, "adauga_reteta.html", {"form": formular})


from django.views.generic import UpdateView

class AlimentUpdateView(UpdateView):
    model = aliment
    form_class = AlimentForm
    template_name = "adauga_aliment.html"
    success_url = reverse_lazy("pagina-alimente")
    
class RetetaUpdateView(UpdateView):
    model = reteta
    form_class = RetetaForm
    template_name = "adauga_reteta.html"
    success_url = reverse_lazy("pagina-retete")    