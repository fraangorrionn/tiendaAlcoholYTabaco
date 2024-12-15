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

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if len(nombre) > 100:
            raise ValidationError("El nombre no debe exceder los 100 caracteres.")
        return nombre

    def clean_correo(self):
        correo = self.cleaned_data.get('correo')
        if not re.match(r"[^@]+@[^@]+\.[^@]+", correo):
            raise ValidationError("El correo electrónico no tiene un formato válido.")
        
        # Validación para que el correo no se repita
        if Usuario.objects.filter(correo=correo).exists():
            raise ValidationError("Ya existe un usuario con este correo electrónico.")
        
        return correo

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono:
            # Validación del formato del teléfono
            if not re.match(r"^\+?\d{7,15}$", telefono):
                raise ValidationError("El teléfono debe tener entre 7 y 15 dígitos y puede incluir un prefijo '+'.")
        return telefono

    def clean(self):
        # Aquí puedes agregar validaciones adicionales si es necesario
        cleaned_data = super().clean()
        return cleaned_data
    
class BusquedaAvanzadaUsuarioForm(forms.Form):
    nombre = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Buscar por nombre'})
    )
    tipo_usuario = forms.MultipleChoiceField(
        choices=Usuario.TIPOS_USUARIO,
        required=False,
        widget=forms.CheckboxSelectMultiple()
    )
    direccion = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Buscar por dirección'})
    )
    
    def clean(self):
        # Lógica de validación personalizada
        super().clean()
        
        # Obtener los datos del formulario
        nombre = self.cleaned_data.get('nombre')
        tipo_usuario = self.cleaned_data.get('tipo_usuario')
        direccion = self.cleaned_data.get('direccion')
        
        # Validar que al menos uno de los campos tenga datos
        if not nombre and not tipo_usuario and not direccion:
            self.add_error('nombre', 'Debe introducir al menos un valor en un campo del formulario.')
            self.add_error('tipo_usuario', 'Debe seleccionar al menos un tipo de usuario.')
            self.add_error('direccion', 'Debe introducir al menos un valor en un campo del formulario.')
        
        # Validar que el nombre tenga al menos 3 caracteres si está presente
        if nombre and len(nombre) < 3:
            self.add_error('nombre', 'Debe introducir al menos 3 caracteres para el nombre.')
        
        # Siempre devolver los datos validados
        return self.cleaned_data
        
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

    def clean_total(self):
        total = self.cleaned_data.get('total')
        if total is None or total <= 0:
            raise ValidationError("El total debe ser mayor a 0.")
        return total

    def clean_metodo_pago(self):
        metodo_pago = self.cleaned_data.get('metodo_pago')
        if not metodo_pago or len(metodo_pago.strip()) == 0:
            raise ValidationError("Debe especificar un método de pago.")
        return metodo_pago

    def clean(self):
        cleaned_data = super().clean()
        estado = cleaned_data.get('estado')
        total = cleaned_data.get('total')

        # Validación adicional: No puede estar pendiente si el total es mayor a 1000 (ejemplo)
        if estado == 'pendiente' and total is not None and total > 1000:
            self.add_error('estado', 'Las órdenes pendientes no pueden tener un total mayor a 1000.')

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
        # Validaciones personalizadas
        super().clean()
        total_min = self.cleaned_data.get('total_min')
        total_max = self.cleaned_data.get('total_max')

        # Validar que total_max sea mayor que total_min si ambos están presentes
        if total_min is not None and total_max is not None and total_max < total_min:
            self.add_error('total_min', 'El total mínimo no puede ser mayor que el total máximo.')
            self.add_error('total_max', 'El total máximo no puede ser menor que el total mínimo.')

        return self.cleaned_data

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

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if Provedor.objects.filter(nombre=nombre).exists():
            raise ValidationError("Ya existe un proveedor con este nombre.")
        return nombre

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if not re.match(r'^\+?\d{7,15}$', telefono):
            raise ValidationError("El teléfono debe tener entre 7 y 15 dígitos y puede incluir un prefijo '+'.")
        return telefono

    def clean_correo(self):
        correo = self.cleaned_data.get('correo')
        if correo and Provedor.objects.filter(correo=correo).exists():
            raise ValidationError("Ya existe un proveedor con este correo electrónico.")
        return correo

    def clean(self):
        cleaned_data = super().clean()
        
        # Asegurarse de que al menos un producto esté seleccionado
        productos = cleaned_data.get('productos')
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
        # Validación personalizada para asegurar al menos un campo completado
        super().clean()
        nombre = self.cleaned_data.get('nombre')
        contacto = self.cleaned_data.get('contacto')
        telefono = self.cleaned_data.get('telefono')

        if not nombre and not contacto and not telefono:
            raise forms.ValidationError("Debe completar al menos un campo para realizar la búsqueda.")

        return self.cleaned_data

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

    def clean_cantidad_disponible(self):
        cantidad_disponible = self.cleaned_data.get('cantidad_disponible')
        if cantidad_disponible is None or cantidad_disponible <= 0:
            raise ValidationError("La cantidad disponible debe ser mayor a 0.")
        return cantidad_disponible

    def clean_minimo_requerido(self):
        minimo_requerido = self.cleaned_data.get('minimo_requerido')
        cantidad_disponible = self.cleaned_data.get('cantidad_disponible')

        # Verificar si ambos campos tienen un valor válido antes de hacer la comparación
        if minimo_requerido is not None and cantidad_disponible is not None:
            if minimo_requerido > cantidad_disponible:
                raise ValidationError("El mínimo requerido no puede ser mayor que la cantidad disponible.")
        return minimo_requerido

    def clean(self):
        cleaned_data = super().clean()
        cantidad_disponible = cleaned_data.get('cantidad_disponible')
        minimo_requerido = cleaned_data.get('minimo_requerido')

        # Validación adicional: Asegurarse de que mínimo requerido no sea mayor que cantidad disponible
        if cantidad_disponible is not None and minimo_requerido is not None:
            if minimo_requerido > cantidad_disponible:
                self.add_error('minimo_requerido', 'El mínimo requerido no puede ser mayor que la cantidad disponible.')

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
        # Validación personalizada
        super().clean()
        cantidad_min = self.cleaned_data.get('cantidad_min')
        cantidad_max = self.cleaned_data.get('cantidad_max')

        # Validar que la cantidad máxima no sea menor que la cantidad mínima
        if cantidad_min is not None and cantidad_max is not None and cantidad_max < cantidad_min:
            self.add_error('cantidad_min', 'La cantidad mínima no puede ser mayor que la cantidad máxima.')
            self.add_error('cantidad_max', 'La cantidad máxima no puede ser menor que la cantidad mínima.')

        return self.cleaned_data
    
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

    def clean_numero_tarjeta(self):
        numero_tarjeta = self.cleaned_data.get('numero_tarjeta')
        
        # Validación para asegurarse de que el número de tarjeta tenga exactamente 16 dígitos
        if len(numero_tarjeta) != 16 or not numero_tarjeta.isdigit():
            raise ValidationError("El número de tarjeta debe tener exactamente 16 dígitos y solo contener números.")
        return numero_tarjeta

    def clean_fecha_expiracion(self):
        fecha_expiracion = self.cleaned_data.get('fecha_expiracion')
        
        # Validación para asegurarse de que la fecha de expiración sea posterior a la fecha actual
        if fecha_expiracion <= date.today():
            raise ValidationError("La tarjeta ha expirado. Debe tener una fecha posterior a hoy.")
        return fecha_expiracion

    def clean_codigo_seguridad(self):
        codigo_seguridad = self.cleaned_data.get('codigo_seguridad')
        
        # Validación para asegurarse de que el código de seguridad tenga entre 3 y 4 dígitos
        if len(codigo_seguridad) < 3 or len(codigo_seguridad) > 4 or not codigo_seguridad.isdigit():
            raise ValidationError("El código de seguridad debe tener entre 3 y 4 dígitos.")
        return codigo_seguridad

    def clean(self):
        cleaned_data = super().clean()

        # Puedes agregar más validaciones si es necesario

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
        # Validaciones personalizadas
        super().clean()
        fecha_inicio = self.cleaned_data.get('fecha_inicio')
        fecha_fin = self.cleaned_data.get('fecha_fin')

        # Validar que la fecha fin no sea anterior a la fecha inicio
        if fecha_inicio and fecha_fin and fecha_fin < fecha_inicio:
            self.add_error('fecha_inicio', 'La fecha desde no puede ser mayor que la fecha hasta.')
            self.add_error('fecha_fin', 'La fecha hasta no puede ser menor que la fecha desde.')

        return self.cleaned_data
        
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

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if Categoria.objects.filter(nombre=nombre).exists():
            raise ValidationError("Ya existe una categoría con este nombre.")
        return nombre

    def clean_estado(self):
        estado = self.cleaned_data.get('estado')
        if estado not in ['activo', 'inactivo']:
            raise ValidationError("El estado debe ser 'activo' o 'inactivo'.")
        return estado

    def clean_prioridad(self):
        prioridad = self.cleaned_data.get('prioridad')
        if prioridad <= 0:
            raise ValidationError("La prioridad debe ser un número mayor que 0.")
        return prioridad

    def clean(self):
        cleaned_data = super().clean()
        # Validación adicional si es necesario
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
        super().clean()
        prioridad_min = self.cleaned_data.get('prioridad_min')
        prioridad_max = self.cleaned_data.get('prioridad_max')

        # Validar que la prioridad máxima no sea menor que la prioridad mínima
        if prioridad_min is not None and prioridad_max is not None and prioridad_max < prioridad_min:
            self.add_error('prioridad_min', 'La prioridad mínima no puede ser mayor que la prioridad máxima.')
            self.add_error('prioridad_max', 'La prioridad máxima no puede ser menor que la prioridad mínima.')

        return self.cleaned_data