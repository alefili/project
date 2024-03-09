from django.db import models

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