from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    ADMINISTRADOR = 1
    CLIENTE = 2
    GERENTE = 3
    ROLES = (
        (ADMINISTRADOR, 'Administrador'),
        (CLIENTE, 'Cliente'),
        (GERENTE, 'Gerente'),
    )

    rol = models.PositiveSmallIntegerField(choices=ROLES, default=CLIENTE)
    direccion = models.CharField(max_length=255, default='sin_direccion')
    telefono = models.CharField(max_length=15, blank=True, null=True)
    productos_favoritos = models.ManyToManyField(
        'Producto',
        through='Favoritos',
        related_name='usuarios_favoritos'
    )

    def __str__(self):
        return self.username
    
class Cliente(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cliente: {self.usuario.username}"


class Gerente(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"Gerente: {self.usuario.username}"


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
    tiempo_estimado_envio = models.TimeField(blank=True, null=True)
    categorias = models.ManyToManyField(
        'Categoria',
        through='ProductoCategoria',
        related_name='productos'
    )
    class Meta:
        permissions = [
            ("ver_productos", "Puede ver productos"),
            ("hacer_pedido", "Puede hacer pedidos"),
            ("ver_ordenes", "Puede ver órdenes"),
            ("gestionar_productos", "Puede gestionar productos"),
        ]

    def __str__(self):
        return self.nombre


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
    archivo_adjunto = models.FileField(upload_to='ordenes_archivos/', null=True, blank=True)

    def __str__(self):
        return f"Orden {self.id} - {self.estado}"


class DetalleOrden(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    descuento_aplicado = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tasa_impuesto = models.FloatField(default=0.0)

    def subtotal(self):
        total = self.cantidad * self.precio_unitario
        descuento = total * (self.descuento_aplicado / 100)
        impuesto = total * (self.tasa_impuesto / 100)
        return total - descuento + impuesto

    def __str__(self):
        return f"Detalle de Orden {self.orden.id} - Producto: {self.producto.nombre}"


class Proveedor(models.Model):  # Corregido
    nombre = models.CharField(max_length=100)
    contacto = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    correo = models.EmailField(blank=True)
    productos = models.ManyToManyField(Producto, related_name='proveedores', blank=True)

    def __str__(self):
        return self.nombre


class Inventario(models.Model):
    producto = models.OneToOneField(Producto, on_delete=models.CASCADE)
    cantidad_disponible = models.IntegerField(verbose_name="Cantidad en inventario")
    ubicacion = models.CharField(max_length=100)
    minimo_requerido = models.IntegerField(default=0)
    fecha_actualizacion = models.DateField(auto_now=True)

    def __str__(self):
        return f"Inventario de {self.producto.nombre}"


class Tarjeta(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    numero_tarjeta = models.CharField(max_length=16)
    fecha_expiracion = models.DateField()
    tipo = models.CharField(max_length=20, default='crédito')
    codigo_seguridad = models.CharField(max_length=4, blank=True)

    def __str__(self):
        return f"Tarjeta de {self.usuario.username}"


class Favoritos(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    fecha_agregado = models.DateField(auto_now_add=True)
    prioridad = models.IntegerField(default=1)
    notas = models.TextField(blank=True)

    def __str__(self):
        return f"Favorito: {self.producto.nombre} de {self.usuario.username}"


class Reclamo(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    detalle_orden = models.OneToOneField(DetalleOrden, on_delete=models.CASCADE, null=True, blank=True)
    descripcion = models.TextField()
    fecha = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=20, default='pendiente')
    respuesta = models.TextField(blank=True)

    def __str__(self):
        return f"Reclamo de {self.usuario.username} - Estado: {self.estado}"


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    fecha_creacion = models.DateField(default=timezone.now)
    estado = models.CharField(max_length=20, default='activo')
    prioridad = models.IntegerField(default=1)

    def __str__(self):
        return self.nombre


class ProductoCategoria(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    fecha_asociacion = models.DateField(auto_now_add=True)
    nota_adicional = models.TextField(blank=True)
    estado = models.CharField(max_length=20, default='activo')

    def __str__(self):
        return f"{self.producto.nombre} en {self.categoria.nombre}"
