from django import forms
from django.forms import ModelForm
from .models import *
from django.core.exceptions import ValidationError
import re
from .models import Usuario, Producto, Orden, Provedor
from datetime import date
import datetime


class UsuarioModelForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['rol', 'direccion', 'telefono', 'productos_favoritos']  # Cambiamos tipo_usuario por rol
        labels = {
            "rol": "Rol del Usuario",
            "direccion": "Dirección",
            "telefono": "Teléfono",
            "productos_favoritos": "Productos Favoritos",
        }
        widgets = {
            "rol": forms.Select(attrs={"class": "form-select"}),  # Cambiamos tipo_usuario por rol
            "direccion": forms.TextInput(attrs={"placeholder": "Dirección completa", "class": "form-control"}),
            "telefono": forms.TextInput(attrs={"placeholder": "Número de teléfono", "class": "form-control"}),
            "productos_favoritos": forms.CheckboxSelectMultiple(),
        }

    def clean(self):
        cleaned_data = super().clean()
        telefono = cleaned_data.get('telefono')

        # Validar teléfono
        if telefono and not re.match(r"^\+?\d{7,15}$", telefono):
            self.add_error('telefono', "El teléfono debe tener entre 7 y 15 dígitos y puede incluir un prefijo '+'.")

        return cleaned_data

    
class BusquedaAvanzadaUsuarioForm(forms.Form):
    rol = forms.MultipleChoiceField(  # Cambiamos tipo_usuario por rol
        choices=Usuario.ROLES,
        required=False,
        widget=forms.CheckboxSelectMultiple()
    )
    direccion = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Buscar por dirección'})
    )
    
    def clean(self):
        cleaned_data = super().clean()
        rol = cleaned_data.get('rol')
        direccion = cleaned_data.get('direccion')

        # Validar que al menos un campo esté lleno
        if not rol and not direccion:
            raise forms.ValidationError("Debe completar al menos un campo para realizar la búsqueda.")

        return cleaned_data

        
class OrdenModelForm(forms.ModelForm):
    class Meta:
        model = Orden
        fields = ['total', 'estado', 'usuario', 'metodo_pago', 'archivo_adjunto']
        labels = {
            'total': 'Total de la Orden',
            'estado': 'Estado de la Orden',
            'usuario': 'Usuario Asociado',
            'metodo_pago': 'Método de Pago',
            'archivo_adjunto': 'Archivo Adjunto',
        }
        widgets = {
            'total': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'usuario': forms.Select(attrs={'class': 'form-select'}),
            'metodo_pago': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Método de Pago'}),
            'archivo_adjunto': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        total = cleaned_data.get('total')
        metodo_pago = cleaned_data.get('metodo_pago')
        estado = cleaned_data.get('estado')

        # Validar total
        if total is None or total <= 0:
            self.add_error('total', "El total debe ser mayor a 0.")

        # Validar método de pago
        if not metodo_pago or len(metodo_pago.strip()) == 0:
            self.add_error('metodo_pago', "Debe especificar un método de pago.")

        # Validación adicional: No puede estar pendiente si el total es mayor a 1000
        if estado == 'pendiente' and total and total > 1000:
            self.add_error('estado', "Las órdenes pendientes no pueden tener un total mayor a 1000.")

        return cleaned_data


class BusquedaAvanzadaOrdenForm(forms.Form):
    estado = forms.ChoiceField(
        choices=[('', 'Todos los estados')] + Orden.ESTADO_ORDEN,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    usuario = forms.ModelChoiceField(
        queryset=Usuario.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    total_min = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Total mínimo'})
    )
    total_max = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Total máximo'})
    )

    def clean(self):
        cleaned_data = super().clean()
        estado = cleaned_data.get('estado')
        usuario = cleaned_data.get('usuario')
        total_min = cleaned_data.get('total_min')
        total_max = cleaned_data.get('total_max')

        # Validar que al menos un campo tenga un valor
        if not estado and not usuario and total_min is None and total_max is None:
            raise forms.ValidationError("Debe introducir al menos un criterio de búsqueda.")

        # Validar que total_max sea mayor que total_min si ambos están presentes
        if total_min is not None and total_max is not None and total_max < total_min:
            self.add_error('total_min', "El total mínimo no puede ser mayor que el total máximo.")
            self.add_error('total_max', "El total máximo no puede ser menor que el total mínimo.")

        return cleaned_data



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

    def clean(self):
        cleaned_data = super().clean()
        nombre = cleaned_data.get('nombre')
        telefono = cleaned_data.get('telefono')
        correo = cleaned_data.get('correo')
        productos = cleaned_data.get('productos')

        # Validar nombre único
        if nombre and Provedor.objects.filter(nombre=nombre).exists():
            self.add_error('nombre', "Ya existe un proveedor con este nombre.")

        # Validar teléfono
        if telefono and not re.match(r'^\+?\d{7,15}$', telefono):
            self.add_error('telefono', "El teléfono debe tener entre 7 y 15 dígitos y puede incluir un prefijo '+'.")

        # Validar correo único
        if correo and Provedor.objects.filter(correo=correo).exists():
            self.add_error('correo', "Ya existe un proveedor con este correo electrónico.")

        # Validar selección de al menos un producto
        if not productos:
            self.add_error('productos', "Debe seleccionar al menos un producto.")

        return cleaned_data

        
class BusquedaAvanzadaProvedorForm(forms.Form):
    nombre = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Buscar por nombre'})
    )
    contacto = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Buscar por contacto'})
    )
    telefono = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Buscar por teléfono'})
    )

    def clean(self):
        cleaned_data = super().clean()
        nombre = cleaned_data.get('nombre')
        contacto = cleaned_data.get('contacto')
        telefono = cleaned_data.get('telefono')

        # Validar que al menos un campo esté lleno
        if not nombre and not contacto and not telefono:
            self.add_error(None, "Debe completar al menos un campo para realizar la búsqueda.")

        return cleaned_data

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

    def clean(self):
        cleaned_data = super().clean()
        cantidad_disponible = cleaned_data.get('cantidad_disponible')
        minimo_requerido = cleaned_data.get('minimo_requerido')

        # Validar cantidad disponible
        if cantidad_disponible is None or cantidad_disponible <= 0:
            self.add_error('cantidad_disponible', "La cantidad disponible debe ser mayor a 0.")

        # Validar que el mínimo requerido no sea mayor que la cantidad disponible
        if minimo_requerido is not None and cantidad_disponible is not None:
            if minimo_requerido > cantidad_disponible:
                self.add_error('minimo_requerido', "El mínimo requerido no puede ser mayor que la cantidad disponible.")

        return cleaned_data

class BusquedaAvanzadaInventarioForm(forms.Form):
    producto = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Buscar por producto'})
    )
    ubicacion = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Buscar por ubicación'})
    )
    cantidad_min = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad mínima'})
    )
    cantidad_max = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad máxima'})
    )

    def clean(self):
        cleaned_data = super().clean()
        cantidad_min = cleaned_data.get('cantidad_min')
        cantidad_max = cleaned_data.get('cantidad_max')

        # Validar que cantidad máxima no sea menor que cantidad mínima
        if cantidad_min is not None and cantidad_max is not None and cantidad_max < cantidad_min:
            self.add_error('cantidad_min', "La cantidad mínima no puede ser mayor que la cantidad máxima.")
            self.add_error('cantidad_max', "La cantidad máxima no puede ser menor que la cantidad mínima.")

        return cleaned_data

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
            'tipo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Crédito/Débito'}),
            'codigo_seguridad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CVV'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        numero_tarjeta = cleaned_data.get('numero_tarjeta')
        fecha_expiracion = cleaned_data.get('fecha_expiracion')
        codigo_seguridad = cleaned_data.get('codigo_seguridad')

        # Validar número de tarjeta
        if numero_tarjeta:
            if len(numero_tarjeta) != 16 or not numero_tarjeta.isdigit():
                self.add_error('numero_tarjeta', "El número de tarjeta debe tener exactamente 16 dígitos y solo contener números.")

        # Validar fecha de expiración
        if fecha_expiracion and fecha_expiracion <= date.today():
            self.add_error('fecha_expiracion', "La tarjeta ha expirado. Debe tener una fecha posterior a hoy.")

        # Validar código de seguridad
        if codigo_seguridad:
            if len(codigo_seguridad) < 3 or len(codigo_seguridad) > 4 or not codigo_seguridad.isdigit():
                self.add_error('codigo_seguridad', "El código de seguridad debe tener entre 3 y 4 dígitos.")

        return cleaned_data

        
class BusquedaAvanzadaTarjetaForm(forms.Form):
    usuario = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Buscar por usuario'})
    )
    tipo = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Buscar por tipo (crédito/débito)'})
    )
    fecha_inicio = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Fecha desde'})
    )
    fecha_fin = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Fecha hasta'})
    )

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')

        # Validar que la fecha fin no sea anterior a la fecha inicio
        if fecha_inicio and fecha_fin and fecha_fin < fecha_inicio:
            self.add_error('fecha_inicio', "La fecha desde no puede ser mayor que la fecha hasta.")
            self.add_error('fecha_fin', "La fecha hasta no puede ser menor que la fecha desde.")

        return cleaned_data

        
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
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'prioridad': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        nombre = cleaned_data.get('nombre')
        estado = cleaned_data.get('estado')
        prioridad = cleaned_data.get('prioridad')

        # Validar nombre único
        if nombre and Categoria.objects.filter(nombre=nombre).exists():
            self.add_error('nombre', "Ya existe una categoría con este nombre.")

        # Validar estado
        if estado and estado not in ['activo', 'inactivo']:
            self.add_error('estado', "El estado debe ser 'activo' o 'inactivo'.")

        # Validar prioridad
        if prioridad is not None and prioridad <= 0:
            self.add_error('prioridad', "La prioridad debe ser un número mayor que 0.")

        return cleaned_data

    
class BusquedaAvanzadaCategoriaForm(forms.Form):
    nombre = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Buscar por nombre'})
    )
    estado = forms.ChoiceField(
        choices=[('', 'Todos los estados'), ('activo', 'Activo'), ('inactivo', 'Inactivo')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    prioridad_min = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Prioridad mínima'})
    )
    prioridad_max = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Prioridad máxima'})
    )

    def clean(self):
        cleaned_data = super().clean()
        prioridad_min = cleaned_data.get('prioridad_min')
        prioridad_max = cleaned_data.get('prioridad_max')

        # Validar que la prioridad máxima no sea menor que la mínima
        if prioridad_min is not None and prioridad_max is not None and prioridad_max < prioridad_min:
            self.add_error('prioridad_min', "La prioridad mínima no puede ser mayor que la prioridad máxima.")
            self.add_error('prioridad_max', "La prioridad máxima no puede ser menor que la prioridad mínima.")

        return cleaned_data
