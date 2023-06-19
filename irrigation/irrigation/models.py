from django.contrib.auth.models import AbstractUser
from django.db import models
import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models.fields.files import ImageField

class User(AbstractUser):
    uid = models.CharField(max_length=255, primary_key=True)
    nom = models.CharField(max_length=255)
    date = models.DateField()
    genre = models.CharField(max_length=10)
    tel = models.CharField(max_length=15)

    def __str__(self):
        return self.username

class Admin(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.email
    

class Farm(models.Model):
    farm_name = models.CharField(max_length=255,default='Default Farm Name')
    location = models.CharField(max_length=255)
    id = models.CharField(max_length=255, primary_key=True)
    User = models.ForeignKey(User, on_delete=models.CASCADE)  
    surface = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    def __str__(self):
        return self.farm_name
    

from django import forms
from .models import Farm

class FarmForm(forms.ModelForm):
    class Meta:
        model = Farm
        fields = ['farm_name', 'location','surface']






from django.db import models
from django import forms

class Plant(models.Model):
    ideal_humidity = models.FloatField()
    ideal_temperature = models.FloatField()
    irrigation_frequency = models.IntegerField()
    name = models.CharField(max_length=100)
    ph_level = models.FloatField()
    plant_id = models.AutoField(primary_key=True)
    plant_type = models.CharField(max_length=100)
    planting_date = models.DateField()
    tree_spacing = models.FloatField()
    trees_per_hectare = models.FloatField()
    image = models.ImageField(upload_to='images/', default='irrigation\irrigation\images\Amandier.jpg')


    def __str__(self):
        return self.name

class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = '__all__'

    def clean_plant_id(self):
        plant_id = self.cleaned_data.get('plant_id')
        if Plant.objects.filter(plant_id=plant_id).exists():
            raise forms.ValidationError("Cet ID de plante est déjà utilisé.")
        return plant_id

class Zone(models.Model):
    zone_id = models.BigAutoField(primary_key=True, default='1')
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    surface = models.DecimalField(max_digits=10, decimal_places=2)
    TYPE_PLANTE_CHOICES = [
        ('herbes', 'Herbes'),
        ('buisson', 'Buisson'),
        ('arbuste', 'Arbuste'),
        ('arbre', 'Arbre'),
    ]
    type_plante = models.CharField(max_length=255, choices=TYPE_PLANTE_CHOICES , default='arbre')
    TYPE_CHOICES = [
        ('serriculture', 'Serriculture'),
        ('en_plein_air', 'En plein air'),
    ]
    type_plantation = models.CharField(max_length=255, choices=TYPE_CHOICES, default='serriculture')
    nombre_portes = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name
  

class ZoneForm(forms.ModelForm):
    class Meta:
        model = Zone
        fields = ['name', 'surface','type_plante','type_plantation','nombre_portes']
