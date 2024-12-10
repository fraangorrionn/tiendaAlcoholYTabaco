from django import forms
from django.forms import ModelForm
from .models import *
from .models import Usuario, Producto, Orden, Provedor
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
        
        
class OrdenModelForm(forms.ModelForm):
    class Meta:
        model = Orden
        fields = ['total', 'estado', 'usuario', 'metodo_pago']
        labels = {
            'total': 'Total de la Orden',
            'estado': 'Estado de la Orden',
            'usuario': 'Usuario Asociado',
            'metodo_pago': 'Método de Pago',
        }
        widgets = {
            'total': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'usuario': forms.Select(attrs={'class': 'form-select'}),
            'metodo_pago': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Método de Pago'}),
        }
        
class ProvedorModelForm(forms.ModelForm):
    class Meta:
        model = Provedor
        fields = ['nombre', 'contacto', 'telefono', 'correo', 'productos']
        labels = {
            'nombre': 'Nombre del Proveedor',
            'contacto': 'Persona de Contacto',
            'telefono': 'Teléfono',
            'correo': 'Correo Electrónico',
            'productos': 'Productos Asociados',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del proveedor'}),
            'contacto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Persona de contacto'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de teléfono'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
            'productos': forms.CheckboxSelectMultiple(),
        }
        
class InventarioModelForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['producto', 'cantidad_disponible', 'ubicacion', 'minimo_requerido']
        labels = {
            'producto': 'Producto',
            'cantidad_disponible': 'Cantidad Disponible',
            'ubicacion': 'Ubicación',
            'minimo_requerido': 'Mínimo Requerido',
        }
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-select'}),
            'cantidad_disponible': forms.NumberInput(attrs={'class': 'form-control'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ubicación del producto'}),
            'minimo_requerido': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        
class TarjetaModelForm(forms.ModelForm):
    class Meta:
        model = Tarjeta
        fields = ['usuario', 'numero_tarjeta', 'fecha_expiracion', 'tipo', 'codigo_seguridad']
        labels = {
            'usuario': 'Usuario',
            'numero_tarjeta': 'Número de Tarjeta',
            'fecha_expiracion': 'Fecha de Expiración',
            'tipo': 'Tipo de Tarjeta',
            'codigo_seguridad': 'Código de Seguridad',
        }
        widgets = {
            'usuario': forms.Select(attrs={'class': 'form-select'}),
            'numero_tarjeta': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de tarjeta'}),
            'fecha_expiracion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'tipo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'crédito/débito'}),
            'codigo_seguridad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CVV'}),
        }
        
class CategoriaModelForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion', 'fecha_creacion', 'estado', 'prioridad']
        labels = {
            'nombre': 'Nombre de la Categoría',
            'descripcion': 'Descripción',
            'fecha_creacion': 'Fecha de Creación',
            'estado': 'Estado',
            'prioridad': 'Prioridad',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la categoría'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'fecha_creacion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'estado': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Activo/Inactivo'}),
            'prioridad': forms.NumberInput(attrs={'class': 'form-control'}),
        }