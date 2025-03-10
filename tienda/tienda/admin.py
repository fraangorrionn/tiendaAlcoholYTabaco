from django.contrib import admin
from .models import (
    Usuario, 
    Producto, 
    Orden, 
    DetalleOrden, 
    Proveedor, 
    Inventario, 
    Tarjeta, 
    Favoritos, 
    Reclamo, 
    Categoria, 
    ProductoCategoria,
    Gerente,
    Cliente
)

# Registro de modelos en el panel de administración
admin.site.register(Usuario)
admin.site.register(Producto)
admin.site.register(Orden)
admin.site.register(DetalleOrden)
admin.site.register(Proveedor)
admin.site.register(Inventario)
admin.site.register(Tarjeta)
admin.site.register(Favoritos)
admin.site.register(Reclamo)
admin.site.register(Categoria)
admin.site.register(ProductoCategoria)
admin.site.register(Gerente)
admin.site.register(Cliente)