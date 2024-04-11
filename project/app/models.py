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
    unitate = models.CharField(max_length=10, choices=UNIT_CHOICES, default = 'buc', db_index=True)
    calorii_unitate = models.DecimalField(max_digits=6, decimal_places=2, default=0, db_index=True)
    
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
        return self.aliment.aggregate(total_calorii=Sum(models.F('retetaaliment__cantitate_aliment') * models.F('retetaaliment__aliment__calorii_unitate')))['total_calorii'] or 0
    
    def aliments_with_quantities(self):
        return self.retetaaliment_set.all()
    
class RetetaAliment(models.Model):
    reteta = models.ForeignKey(Reteta, on_delete=models.CASCADE)
    aliment = models.ForeignKey(Aliment, on_delete=models.CASCADE)
    cantitate_aliment = models.DecimalField(max_digits=6, decimal_places=2, default=0, db_index=True)

class UserProfile(models.Model):
    GENDER_CHOICES = (
        ('f', 'feminin'),
        ('m', 'masculin'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    greutate = models.IntegerField(default=0, db_index=True)
    inaltime = models.IntegerField(default=0, db_index=True)
    varsta = models.IntegerField(default=0, db_index=True)
    genul = models.CharField(max_length=10, choices=GENDER_CHOICES, default = 'm', db_index=True)
    
    def ideal_calorii(self):
        if UserProfile.genul == 'f':
            return '2000 calorii'
        else:
            return '2500 calorii' 
          
class Plan(models.Model):
    ziua = models.DateField(unique=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    reteta = models.ManyToManyField(Reteta, through='PlanReteta', blank=True)
    aliment = models.ManyToManyField(Aliment, through='PlanAliment', blank=True)

    def __str__(self):
        return f"Plan {self.ziua}"
    
    def calculate_total_calories(self):
        total_calorii_retete = self.reteta.aggregate(total_calorii=Sum(models.F('plan__cantitate_reteta') * models.F('plan__reteta__calorii')))['total_calorii'] or 0
        total_calorii_alimente = self.aliment.aggregate(total_calories=Sum(models.F('plan__cantitate_aliment') * models.F('plan__aliment__calorii')))['total_calories'] or 0
        return total_calorii_retete + total_calorii_alimente
        
class PlanReteta(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    reteta = models.ForeignKey(Reteta, on_delete=models.CASCADE)
    cantitate_reteta = models.DecimalField(max_digits=6, decimal_places=2, default=0, db_index=True)

class PlanAliment(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    aliment = models.ForeignKey(Aliment, on_delete=models.CASCADE)
    cantitate_aliment = models.DecimalField(max_digits=6, decimal_places=2, default=0, db_index=True)   
        

