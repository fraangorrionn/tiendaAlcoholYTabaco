from rest_framework import serializers
from .models import Producto, Categoria, ProductoCategoria, Inventario, Orden, Proveedor, DetalleOrden, Reclamo

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
        return obj.productocategoria_set.values_list('categoria__nombre', flat=True)

    def get_cantidad_disponible(self, obj):
        inventario = getattr(obj, 'inventario', None)
        return inventario.cantidad_disponible if inventario else 0

# Serializador para los detalles de una orden
class DetalleOrdenSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre')

    class Meta:
        model = DetalleOrden
        fields = ['producto_nombre', 'cantidad', 'precio_unitario']

# Serializador para las órdenes con productos y usuario
class OrdenSerializer(serializers.ModelSerializer):
    usuario = serializers.CharField(source='usuario.username')
    productos = DetalleOrdenSerializer(source='detalleorden_set', many=True)

    class Meta:
        model = Orden
        fields = ['id', 'fecha_orden', 'total', 'estado', 'usuario', 'productos']

# Serializador para los proveedores con sus productos
class ProveedorSerializer(serializers.ModelSerializer):
    productos = serializers.StringRelatedField(many=True)  # Lista de productos en texto

    class Meta:
        model = Proveedor
        fields = ['nombre', 'contacto', 'telefono', 'productos']
        

class ReclamoSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.CharField(source='usuario.username', read_only=True)
    producto_nombre = serializers.CharField(source='detalle_orden.producto.nombre', read_only=True)

    class Meta:
        model = Reclamo
        fields = ['id', 'usuario', 'usuario_nombre', 'producto_nombre', 'descripcion', 'fecha', 'estado', 'respuesta']
        
class BusquedaProductoSerializer(serializers.Serializer):
    nombre = serializers.CharField(required=False, max_length=100)
    tipo = serializers.ChoiceField(choices=Producto.TIPO_PRODUCTO, required=False)
    precio_min = serializers.DecimalField(required=False, max_digits=10, decimal_places=2)
    precio_max = serializers.DecimalField(required=False, max_digits=10, decimal_places=2)

    def validate(self, data):
        if 'precio_min' in data and 'precio_max' in data:
            if data['precio_min'] > data['precio_max']:
                raise serializers.ValidationError("El precio mínimo no puede ser mayor que el máximo.")
        return data
