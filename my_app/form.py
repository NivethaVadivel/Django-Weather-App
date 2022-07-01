from dataclasses import fields
from pyexpat import model
from django.forms import ModelForm,TextInput
from .models import City

class CityForm(ModelForm):
    class Meta:
        model=City
        fields=["name"]
        widgets={'name':TextInput(attrs={'class':'form-control','placeholder':'City Name'})}