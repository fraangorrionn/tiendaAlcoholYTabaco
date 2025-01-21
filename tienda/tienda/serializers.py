from rest_framework import serializers
from .models import *
from .forms import *

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email']  # Ajusta según los campos relevantes

class OrdenSerializer(serializers.ModelSerializer):
    # Relación con el usuario
    usuario = UsuarioSerializer(read_only=True)  # Serializa el usuario completo (anidado)

    # Para formatear la fecha de creación de la orden
    fecha_orden = serializers.DateField(format='%d-%m-%Y', read_only=True)

    # Para obtener el valor legible de los choices
    estado = serializers.CharField(source='get_estado_display', read_only=True)

    class Meta:
        model = Orden
        fields = [
            'id', 'fecha_orden', 'total', 'estado', 'usuario',
            'metodo_pago'
        ]
