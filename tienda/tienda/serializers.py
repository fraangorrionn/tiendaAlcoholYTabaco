from rest_framework import serializers
from .models import *
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


class OrdenSerializerCreate(serializers.ModelSerializer):
    
    ESTADO_OPCIONES = [("", "Ninguno")] + Orden.ESTADO_ORDEN
    estado = serializers.ChoiceField(choices=ESTADO_OPCIONES)

    class Meta:
        model = Orden
        fields = '__all__'

    def validate_total(self, total):
        # Validar que el total de la orden sea mayor que 0.
        
        if total <= 0:
            raise serializers.ValidationError("El total debe ser mayor que 0.")
        return total

    def validate_usuario(self, usuario):
        # Validar que el usuario sea válido.
        
        if not Usuario.objects.filter(id=usuario.id).exists():
            raise serializers.ValidationError("El usuario seleccionado no existe.")
        return usuario

    def validate_estado(self, estado):
        # Validar que se seleccione un estado válido.
        
        if estado == "":
            raise serializers.ValidationError("Debe seleccionar un estado válido para la orden.")
        return estado

class ProveedorSerializerCreate(serializers.ModelSerializer):
    
    class Meta:
        model = Proveedor
        fields = '__all__'

    def validate_nombre(self, nombre):
        # Validar que el nombre del proveedor no esté vacío y no se repita.
        
        if not nombre.strip():
            raise serializers.ValidationError("El nombre del proveedor no puede estar vacío.")

        existe_nombre = Proveedor.objects.filter(nombre=nombre).first()
        if existe_nombre:
            if self.instance and existe_nombre.id == self.instance.id:
                pass
            else:
                raise serializers.ValidationError("Ya existe un proveedor con ese nombre.")
        return nombre

    def validate_telefono(self, telefono):
        # Validar que el teléfono tenga al menos 9 dígitos.

        if len(telefono) < 9:
            raise serializers.ValidationError("El número de teléfono debe tener al menos 9 dígitos.")
        return telefono

    def validate_productos(self, productos):
        # Validar que al menos un producto esté asociado.

        if not productos:
            raise serializers.ValidationError("Debe asociar al menos un producto al proveedor.")
        return productos
    
class FavoritosSerializerCreate(serializers.ModelSerializer):

    class Meta:
        model = Favoritos
        fields = ['usuario', 'producto', 'prioridad', 'notas']

    def validate_usuario(self, usuario):
        # Validar que el usuario existe en la base de datos.
        
        if not Usuario.objects.filter(id=usuario.id).exists():
            raise serializers.ValidationError("El usuario seleccionado no existe.")
        return usuario

    def validate_producto(self, producto):
        # Validar que el producto existe en la base de datos.

        if not Producto.objects.filter(id=producto.id).exists():
            raise serializers.ValidationError("El producto seleccionado no existe.")
        return producto

    def validate_prioridad(self, prioridad):
        # Validar que la prioridad esté dentro del rango permitido (1 a 5).
    
        if prioridad < 1 or prioridad > 5:
            raise serializers.ValidationError("La prioridad debe estar entre 1 y 5.")
        return prioridad

    def create(self, validated_data):
        # Crear una nueva entrada en Favoritos.
        
        return Favoritos.objects.create(**validated_data)


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

class OrdenActualizarEstadoSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Orden
        fields = ['estado']
    
    def validate_estado(self, estado):
        # Validar que el estado sea uno de los permitidos.
    
        if estado not in dict(Orden.ESTADO_ORDEN):
            raise serializers.ValidationError('Estado no válido.')
        return estado
    
class ProveedorActualizarContactoSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Proveedor
        fields = ['contacto']
    
    def validate_contacto(self, contacto): 
        if len(contacto) < 3:
            raise serializers.ValidationError('El contacto debe tener al menos 3 caracteres.')
        return contacto

class FavoritosSerializerActualizarPrioridad(serializers.ModelSerializer):

    class Meta:
        model = Favoritos
        fields = ['prioridad', 'notas']

    def validate_prioridad(self, prioridad):
        # Validar que la prioridad esté dentro del rango permitido (1 a 5).
        if prioridad < 1 or prioridad > 5:
            raise serializers.ValidationError("La prioridad debe estar entre 1 y 5.")
        return prioridad
