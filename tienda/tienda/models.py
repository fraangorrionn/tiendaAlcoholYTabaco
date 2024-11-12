from django.db import models
from django.utils import timezone

class Usuario(models.Model):
    TIPOS_USUARIO = [
        ('cliente', 'Cliente'),
        ('administrador', 'Administrador'),
    ]
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(default='default@example.com')
    direccion = models.CharField(max_length=255, default='sin_direccion')
    tipo_usuario = models.CharField(max_length=50, choices=TIPOS_USUARIO, null=True)
    telefono = models.CharField(max_length=15, blank=True)
    productos_favoritos = models.ManyToManyField('Producto', through='Favoritos', related_name='usuarios_favoritos')

class Producto(models.Model):
    TIPO_PRODUCTO = [
        ('vino', 'Vino'),
        ('cerveza', 'Cerveza'),
        ('tabaco', 'Tabaco'),
    ]
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=20, choices=TIPO_PRODUCTO, default='vino')
    stock = models.IntegerField(default=0)
    descripcion = models.TextField(blank=True)
    tiempo_estimado_envio = models.TimeField(blank=True, null=True)  # Nuevo campo TimeField
    categorias = models.ManyToManyField('Categoria', through='ProductoCategoria', related_name='productos')


class Orden(models.Model):
    ESTADO_ORDEN = [
        ('completada', 'Completada'),
        ('pendiente', 'Pendiente'),
        ('cancelada', 'Cancelada'),
    ]
    fecha_orden = models.DateField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADO_ORDEN)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    metodo_pago = models.CharField(max_length=50, blank=True)


class DetalleOrden(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    descuento_aplicado = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tasa_impuesto = models.FloatField(default=0.0) 

class Provedor(models.Model):
    nombre = models.CharField(max_length=100)
    contacto = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    correo = models.EmailField(blank=True)
    productos = models.ManyToManyField(Producto, related_name='provedores', blank=True)

class Inventario(models.Model):
    producto = models.OneToOneField(Producto, on_delete=models.CASCADE)
    cantidad_disponible = models.IntegerField(verbose_name="Cantidad en inventario")
    ubicacion = models.CharField(max_length=100)
    minimo_requerido = models.IntegerField(default=0)
    fecha_actualizacion = models.DateField(auto_now=True)

class Tarjeta(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    numero_tarjeta = models.CharField(max_length=16)
    fecha_expiracion = models.DateField()
    tipo = models.CharField(max_length=20, default='crédito') 
    codigo_seguridad = models.CharField(max_length=4, blank=True)
    
class Favoritos(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    fecha_agregado = models.DateField(auto_now_add=True)
    prioridad = models.IntegerField(default=1)
    notas = models.TextField(blank=True)

class Reclamo(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    detalle_orden = models.OneToOneField(DetalleOrden, on_delete=models.CASCADE, null=True, blank=True)  # Nueva relación OneToOne con DetalleOrden
    descripcion = models.TextField()
    fecha = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=20, default='pendiente')
    respuesta = models.TextField(blank=True)

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    fecha_creacion = models.DateField(default=timezone.now)
    estado = models.CharField(max_length=20, default='activo')  
    prioridad = models.IntegerField(default=1)

class ProductoCategoria(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    fecha_asociacion = models.DateField(auto_now_add=True)
    nota_adicional = models.TextField(blank=True)
    estado = models.CharField(max_length=20, default='activo')
