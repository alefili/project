from django import forms
from django.contrib.auth import authenticate
from django.forms import ValidationError
from django.contrib.auth.models import User
from tinymce.widgets import TinyMCE

from .models import Aliment, Plan, UserProfile

class ContactForm(forms.Form):
    email = forms.EmailField(required=True)
    subiect = forms.CharField(label="Subiectul tau")
    mesaj = forms.CharField(widget=forms.Textarea())
    trimite_copie = forms.BooleanField(required=False)

    def clean_email(self):
        email = self.cleaned_data["email"]
        if not email.endswith("@gmail.com"):
            raise forms.ValidationError("Email invalid!")
        return email

class CustomLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = authenticate(None, username=username, password=password)
        if user is  None:
            raise forms.ValidationError('Nu exista User-ul')
        else:
            self.authenticate_user = user
        return self.cleaned_data

class RegistrationForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['genul']
    
class AlimentForm(forms.ModelForm):
    class Meta:
        model = Aliment
        fields = "__all__"
        
        
class PlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ['aliment', 'cantitate_aliment', 'target_calorii']
        widgets = {
            'aliment': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'cantitate_aliment': forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_cantitate_aliment'}),
            'target_calorii': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            daily_consumption = Plan.objects.create(user=instance.plan.user.user, food_item=instance.aliment, quantity=instance.cantitate_aliment)
            daily_consumption.save()
        return instance
        
    