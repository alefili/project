from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.db.models import Sum
import json

from .forms import *
from .decorators import is_staff
from .models import Aliment, Plan

from django.db.models import F

# Create your views here.
def welcome(request):
    if request.method == 'POST':
        target_calorii = request.POST.get('target_calorii')
        submitted_data = []
        
        total_calorii = 0

        # Iterate through submitted aliment quantities
        for key, value in request.POST.items():
            if key.startswith('aliment_') and value:
                aliment_id = key.split('_')[1]
                aliment = Aliment.objects.get(id=aliment_id)
                cantitate_aliment = value
                
                calorii = aliment.calorii_unitate * int(cantitate_aliment)
                total_calorii += calorii
                
                submitted_data.append({
                    'aliment': aliment, 
                    'cantitate_aliment': cantitate_aliment,
                    'calorii': calorii
                })

        context = {
            'target_calorii': target_calorii,
            'submitted_data': submitted_data,
            'aliments': Aliment.objects.all(),
            'total_calorii': total_calorii,  # Pass total calories to the template
}

        return render(request, 'index.html', context)


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
    

def custom_login(request):
    login_form = CustomLoginForm()
    registration_form = RegistrationForm()
    profile_form = UserProfileForm()  # Add this line to create an instance of UserProfileForm
    if request.method == 'POST':
        if 'login_submit' in request.POST:
            login_form = CustomLoginForm(request.POST)
            if login_form.is_valid():
                login(request, login_form.authenticate_user)
                return redirect("/")
        elif 'registration_submit' in request.POST:
            registration_form = RegistrationForm(request.POST)
            profile_form = UserProfileForm(request.POST)  # Add this line to bind form data to UserProfileForm
            if registration_form.is_valid() and profile_form.is_valid():
                # Create a new user
                username = registration_form.cleaned_data['username']
                password = registration_form.cleaned_data['password']
                user = User.objects.create_user(username=username, password=password)
                # Create a new user profile and associate it with the user
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()
                # Login the new user
                login(request, user)
                return redirect("/")
    return render(request, 'login.html', {'login_form': login_form, 'registration_form': registration_form, 'profile_form': profile_form})

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
def plan(request, id):
    plan = get_object_or_404(Plan, id=id)
    consumed_calories = plan.calculate_total_calories()
    daily_target = plan.user.target_calorii()  # Assuming you have a method to retrieve the daily calorie target
    remaining_calories = daily_target - consumed_calories
    return render(request, "plan.html", {"plan": plan, "remaining_calories": remaining_calories})

@is_staff
@login_required
def adauga_plan(request):
    formular = PlanForm()
    if request.method == "POST":
        formular = PlanForm(request.POST)
        if formular.is_valid():
            formular.save()
            return redirect(reverse("pagina-planuri"))
    return render(request, "adauga_plan.html", {"form": formular})

from django.views.generic import UpdateView

class AlimentUpdateView(UpdateView):
    model = aliment
    form_class = AlimentForm
    template_name = "adauga_aliment.html"
    success_url = reverse_lazy("pagina-alimente") 
    
class PlanUpdateView(UpdateView):
    model = plan
    form_class = PlanForm
    template_name = "adauga_plan.html"
    success_url = reverse_lazy("pagina-planuri")  