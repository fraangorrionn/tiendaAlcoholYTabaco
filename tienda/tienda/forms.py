from django import forms
from django.forms import ModelForm
from .models import *
from datetime import date
import datetime


class UsuarioModelForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'correo', 'direccion', 'tipo_usuario', 'telefono', 'productos_favoritos']
        labels = {
            "nombre": "Nombre del Usuario",
            "correo": "Correo Electrónico",
            "direccion": "Dirección",
            "tipo_usuario": "Tipo de Usuario",
            "telefono": "Teléfono",
            "productos_favoritos": "Productos Favoritos",
        }
        help_texts = {
            "nombre": "Máximo 100 caracteres.",
            "correo": "Debe tener un formato válido (ejemplo: usuario@example.com).",
            "productos_favoritos": "Selecciona uno o más productos favoritos.",
        }
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre del usuario"}),
            "correo": forms.EmailInput(attrs={"class": "form-control", "placeholder": "usuario@example.com"}),
            "direccion": forms.TextInput(attrs={"placeholder": "Dirección completa", "class": "form-control"}),
            "tipo_usuario": forms.Select(attrs={"class": "form-select"}),
            "telefono": forms.TextInput(attrs={"placeholder": "Número de teléfono", "class": "form-control"}),
            "productos_favoritos": forms.CheckboxSelectMultiple(),
        }
        