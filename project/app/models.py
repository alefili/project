from django.db import models

# Create your models here.
class Aliment(models.Model):
    titlu = models.CharField(max_length=50, unique=True)
    stoc = models.IntegerField(default=0, db_index=True)
    calorii = models.IntegerField(default=0, db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Aliment {self.titlu} "
    
class Retete(models.Model):
    aliment = models.ForeignKey(Aliment, null=True, blank=True, on_delete=models.CASCADE)
    nume = models.CharField(max_length=50)

    def __str__(self):
        return f"Retete {self.nume}"