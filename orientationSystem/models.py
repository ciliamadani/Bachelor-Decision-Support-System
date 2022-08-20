from django.db import models

# Create your models here.
class Bachelier(models.Model):
    matricule =  models.CharField(max_length = 100 ,blank=True, default='')
    serie_bac =  models.CharField(max_length = 15, blank=True, default='')
    annee_bac = models.IntegerField(default=2022)
    moyenne_bac = models.DecimalField(max_digits = 5, decimal_places = 2,default=0.0)
    sexe =  models.CharField(max_length = 15, blank=True, default='')
    english = models.DecimalField(max_digits = 5, decimal_places = 2,default=0.0)
    french = models.DecimalField(max_digits = 5, decimal_places = 2,default=0.0)
    his_geo = models.DecimalField(max_digits = 5, decimal_places = 2,default=0.0)
    arabic_literature = models.DecimalField(max_digits = 5, decimal_places = 2,default=0.0)
    maths = models.DecimalField(max_digits = 5, decimal_places = 2,default=0.0)
    philosophy = models.DecimalField(max_digits = 5, decimal_places = 2,default=0.0)
    physics = models.DecimalField(max_digits = 5, decimal_places = 2,default=0.0)
    primary_module = models.DecimalField(max_digits = 5, decimal_places = 2,default=0.0)
    islamic_science = models.DecimalField(max_digits = 5, decimal_places = 2,default=0.0)
    
    
