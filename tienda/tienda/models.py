from django.db import models

class Usuario(models.Model):
    TIPOS_USUARIO = [
        ('cliente', 'Cliente'),
        ('administrador', 'Administrador'),
    ]
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True, default='default@example.com')  # Campo 'correo' con valor por defecto
    direccion = models.CharField(max_length=255, default='sin_direccion')  # Aquí se añade el valor por defecto
    tipo_usuario = models.CharField(max_length=50, null=True)
    telefono = models.CharField(max_length=15, blank=True)

class Producto(models.Model):
    TIPO_PRODUCTO = [
        ('vino', 'Vino'),
        ('cerveza', 'Cerveza'),
        ('tabaco', 'Tabaco'),
    ]
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=20, choices=TIPO_PRODUCTO, default='vino')  # Aquí se añade el valor por defecto
    stock = models.IntegerField(default=0)
    descripcion = models.TextField(blank=True)  # Descripción del producto

class Orden(models.Model):
    ESTADO_ORDEN = [
        ('completada', 'Completada'),
        ('pendiente', 'Pendiente'),
        ('cancelada', 'Cancelada'),
    ]
    
    fecha_orden = models.DateField(auto_now_add=True)  # Fecha de la orden
    total = models.DecimalField(max_digits=10, decimal_places=2)  # Total de la orden
    estado = models.CharField(max_length=20, choices=ESTADO_ORDEN)  # Estado de la orden
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)  # Relación con el usuario
    metodo_pago = models.CharField(max_length=50, blank=True)  # Método de pago

class DetalleOrden(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE)  # Relación con la orden
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)  # Relación con el producto
    cantidad = models.IntegerField(default=1)  # Cantidad del producto en la orden
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)  # Precio unitario del producto
    descuento_aplicado = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Descuento aplicado

class Provedor(models.Model):
    nombre = models.CharField(max_length=100)  # Nombre del proveedor
    contacto = models.CharField(max_length=100)  # Nombre de contacto
    telefono = models.CharField(max_length=15)  # Teléfono del proveedor
    correo = models.EmailField(blank=True)  # Correo electrónico del proveedor (opcional)

class Inventario(models.Model):
    producto = models.OneToOneField(Producto, on_delete=models.CASCADE)  # Relación uno a uno con el producto
    cantidad_disponible = models.IntegerField()  # Cantidad disponible del producto en inventario
    ubicacion = models.CharField(max_length=100)  # Ubicación del producto en el inventario
    minimo_requerido = models.IntegerField(default=0)  # Cantidad mínima requerida

class Tarjeta(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    numero_tarjeta = models.CharField(max_length=16)
    fecha_expiracion = models.DateField()
    tipo = models.CharField(max_length=20, default='crédito') 
    
class Favoritos(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)  # Relación con el usuario
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)  # Relación con el producto
    fecha_agregado = models.DateField(auto_now_add=True)  # Fecha en que se agregó a favoritos
    prioridad = models.IntegerField(default=1)  # Prioridad en favoritos

class Reclamo(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)  # Relación uno a uno con el usuario
    descripcion = models.TextField()  # Descripción del reclamo
    fecha = models.DateField(auto_now_add=True)  # Fecha del reclamo
    estado = models.CharField(max_length=20, default='pendiente')  # Estado del reclamo

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)  # Nombre de la categoría (único)
    descripcion = models.TextField(blank=True)  # Descripción de la categoría

class ProductoCategoria(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)  # Relación con el producto
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)  # Relación con la categoría
    fecha_asociacion = models.DateField(auto_now_add=True)  # Fecha de asociación del producto con la categoría
    nota_adicional = models.TextField(blank=True)  # Nota adicional sobre la asociación
