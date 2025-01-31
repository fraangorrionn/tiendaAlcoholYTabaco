from rest_framework import serializers
from .models import Producto, Categoria, ProductoCategoria, Inventario

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'precio', 'tipo', 'stock']


class ProductoDetalleSerializer(serializers.ModelSerializer):
    categorias = serializers.SerializerMethodField()
    cantidad_disponible = serializers.SerializerMethodField()

    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'precio', 'tipo', 'stock', 'categorias', 'cantidad_disponible']

    def get_categorias(self, obj):
        categorias = ProductoCategoria.objects.filter(producto=obj).select_related('categoria')
        return [categoria.categoria.nombre for categoria in categorias]

    def get_cantidad_disponible(self, obj):
        inventario = Inventario.objects.filter(producto=obj).first()
        return inventario.cantidad_disponible if inventario else 0