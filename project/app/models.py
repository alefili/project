from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Aliment(models.Model):
    UNIT_CHOICES = (
        ('l', 'Litru'),
        ('ml', 'Mililitru'),
        ('g', 'Gram'),
        ('kg', 'Kilogram'),
        ('buc', 'Bucata'),
    )
    titlu = models.CharField(max_length=50, unique=True)
    stoc = models.IntegerField(default=0, db_index=True)
    unitate = models.CharField(max_length=10, choices=UNIT_CHOICES, default = 'buc', db_index=True)
    calorii = models.IntegerField(default=0, db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Aliment {self.titlu} "
    
class Reteta(models.Model):
    aliment = models.ForeignKey(Aliment, null=True, blank=True, on_delete=models.CASCADE)
    nume = models.CharField(max_length=50)
    calorii = models.CharField(max_length=50)
    indicatii = models.CharField(max_length=1024, null=True, blank=True, help_text="Introduceti indicatii")

    def __str__(self):
        return f"Retete {self.nume}"
    
class Plan(models.Model):
    reteta = models.ForeignKey(Reteta, null=True, blank=True, on_delete=models.CASCADE)
    calorii = models.CharField(max_length=50)
    ziua = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Plan {self.nume}"
    
class Cumparaturi(models.Model):
    aliment = models.ForeignKey(Aliment, null=True, blank=True, on_delete=models.CASCADE)
    cantitate = models.IntegerField(default=0, db_index=True)

    def __str__(self):
        return f"Cumparaturi {self.nume}"
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefon = models.CharField(max_length=15)
    adresa = models.CharField(max_length=100)
    oras = models.CharField(max_length=20)
    cnp = models.CharField(max_length=13, null=True, blank=True)
    
class PlanPersonalizat(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    cumparaturi = models.ForeignKey(Cumparaturi, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)