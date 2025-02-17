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


#---------------------------------------------------------POST-------------------------------------------------------

class ProductoCreateSerializer(serializers.ModelSerializer):

    TIPO_PRODUCTO_OPCIONES = [("", "Ninguno")] + Producto.TIPO_PRODUCTO
    tipo = serializers.ChoiceField(choices=TIPO_PRODUCTO_OPCIONES)

    class Meta:
        model = Producto
        fields = ['nombre', 'precio', 'tipo', 'stock', 'descripcion']

    def validate_nombre(self, nombre):
        # Validar que el nombre del producto no esté vacío y no se repita.
        
        if not nombre.strip():
            raise serializers.ValidationError("El nombre del producto no puede estar vacío.")

        existe_nombre = Producto.objects.filter(nombre=nombre).first()
        if existe_nombre:
            if self.instance and existe_nombre.id == self.instance.id:
                pass
            else:
                raise serializers.ValidationError("Ya existe un producto con ese nombre.")
        return nombre

    def validate_precio(self, precio):
        # Validar que el precio sea mayor que 0.
        
        if precio <= 0:
            raise serializers.ValidationError("El precio debe ser mayor que 0.")
        return precio

    def validate_stock(self, stock):
        # Validar que el stock sea un número positivo.
        
        if stock < 0:
            raise serializers.ValidationError("El stock no puede ser negativo.")
        return stock

    def validate_tipo(self, tipo):
        # Validar que el tipo de producto sea una opción válida.
        
        if tipo == "":
            raise serializers.ValidationError("Debes seleccionar un tipo de producto.")
        return tipo

#---------------------------------------------------------PATCH-------------------------------------------------------

class ProductoActualizarNombreSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Producto
        fields = ['nombre']
    
    def validate_nombre(self, nombre):
        # Validar que el nombre no esté repetido en otro producto.
        
        producto_existente = Producto.objects.filter(nombre=nombre).first()
        if producto_existente and self.instance and producto_existente.id != self.instance.id:
            raise serializers.ValidationError('Ya existe un producto con ese nombre.')
        return nombre
