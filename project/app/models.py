from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum, F

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
    caloriiunitate = models.DecimalField(max_digits=6, decimal_places=2, default=0, db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Aliment {self.titlu} "
    
class Reteta(models.Model):
    aliment = models.ManyToManyField(Aliment, through='RetetaAliment')
    nume = models.CharField(max_length=50)
    indicatii = models.CharField(max_length=1024, null=True, blank=True, help_text="Introduceti indicatii")

    def __str__(self):
        return f"Retete {self.nume}"
    
    @property
    def calorii(self):
        calorii = 0
        alimente = self.retetaaliment_set.all()
        for aliment in alimente:
            calorii +=aliment.cantitate_aliment * RetetaAliment.aliment.caloriiunitate
    
    def calculator_total_calorii(self):
        return self.aliment.aggregate(total_calorii=Sum(models.F('retetaaliment__cantitate_aliment') * models.F('retetaaliment__aliment__caloriiunitate')))['total_calorii'] or 0
    
    def aliments_with_quantities(self):
        return self.retetaaliment_set.all()
    
class RetetaAliment(models.Model):
    reteta = models.ForeignKey(Reteta, on_delete=models.CASCADE)
    aliment = models.ForeignKey(Aliment, on_delete=models.CASCADE)
    cantitate_aliment = models.DecimalField(max_digits=6, decimal_places=2, default=0, db_index=True)
    
class Plan(models.Model):
    calorii = models.CharField(max_length=50)
    ziua = models.DateTimeField(auto_now=True)
    reteta = models.ManyToManyField(Reteta)
    cantitate_reteta = models.DecimalField(max_digits=6, decimal_places=2, default=0, db_index=True)
    aliment = models.ManyToManyField(Aliment, through='MealPlanAliment')
    cantitate_aliment = models.DecimalField(max_digits=6, decimal_places=2, default=0, db_index=True)

    def __str__(self):
        return f"Plan {self.ziua}"
    
    def calculate_total_calories(self):
        total_calorii_retete = self.reteta.aggregate(total_calorii=Sum('plan__cantitate_reteta' * 'plan__reteta__calorii'))['total_calorii'] or 0
        total_calorii_alimente = self.aliment.aggregate(total_calories=Sum('plan__cantitate_aliment' * 'plan__aliment__calorii'))['total_calories'] or 0
        return total_calorii_retete + total_calorii_alimente
    
       
class MealPlanAliment(models.Model):
    meal_plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    aliment = models.ForeignKey(Aliment, on_delete=models.CASCADE)
    cantitate_aliment = models.DecimalField(max_digits=6, decimal_places=2, default=0, db_index=True)

        
    
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
    
    def calculate_shopping_list(self):
        shopping_list = {}
        for cumparaturi_item in self.cumparaturi.all():
            aliment = cumparaturi_item.aliment
            needed_quantity = cumparaturi_item.cantitate
            available_quantity = aliment.stoc
            if available_quantity < needed_quantity:
                shopping_list[aliment.titlu] = needed_quantity - available_quantity
        return shopping_list