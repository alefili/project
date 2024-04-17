from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum, F
from django.utils import timezone

# Create your models here.
class Aliment(models.Model):
    titlu = models.CharField(max_length=50, unique=True)
    calorii = models.DecimalField(max_digits=6, decimal_places=2, default=0, db_index=True)
    proteine = models.DecimalField(max_digits=6, decimal_places=2, default=0, db_index=True)
    lipide = models.DecimalField(max_digits=6, decimal_places=2, default=0, db_index=True)
    glucide = models.DecimalField(max_digits=6, decimal_places=2, default=0, db_index=True)
    apa = models.DecimalField(max_digits=6, decimal_places=2, default=0, db_index=True)
    
    def __str__(self):
        return f"Aliment {self.titlu} "
    
class UserProfile(models.Model):
    GENDER_CHOICES = (
        ('f', 'feminin'),
        ('m', 'masculin'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    genul = models.CharField(max_length=10, choices=GENDER_CHOICES, default = 'm', db_index=True)
    
    
    def ideal_calorii(self):
        if UserProfile.genul == 'feminin':
            return '2000'
        else:
            return '2500' 
          
class Plan(models.Model):
    ziua = models.DateField(unique=True, default=timezone.now)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    aliment = models.ManyToManyField(Aliment, blank=True)
    cantitate_aliment = models.DecimalField(max_digits=6, decimal_places=2, default=0, db_index=True)  
    calculate_total_calories = models.IntegerField(default=0) 
    calorii_ramase = models.IntegerField(default=0)
    target_calorii = models.IntegerField(default=UserProfile.ideal_calorii(user))
    
    def __str__(self):
        return f"Plan {self.ziua}"
    
    def save(self, *args, **kwargs):
        self.calculate_total_calories = self.calculate_total_calories()
        self.calorii_ramase = self.calorii_ramase()
        super().save(*args, **kwargs)
    
    def calculate_total_calories(self):
        total_calorii_alimente = self.aliment.aggregate(total_calories=Sum(models.F('plan__cantitate_aliment') * models.F('plan__aliment__calorii')))['total_calories'] or 0
        return total_calorii_alimente
    
    def calorii_ramase(self):
        return self.target_calorii - self.calculate_total_calories
        