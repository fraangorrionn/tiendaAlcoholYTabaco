from django.urls import path
from .views import (
    index, lista_usuario, lista_producto, lista_orden,
    lista_detalle_orden, lista_provedor, lista_inventario,
    lista_tarjeta, lista_favoritos, lista_reclamo,
    lista_categoria, lista_producto_categoria
)

urlpatterns = [
    path('', index, name='index'),
    path('usuarios/', lista_usuario, name='lista_usuario'),
    path('productos/', lista_producto, name='lista_producto'),
    path('ordenes/', lista_orden, name='lista_orden'),
    path('detalles-orden/', lista_detalle_orden, name='lista_detalle_orden'),
    path('provedores/', lista_provedor, name='lista_provedor'),
    path('inventarios/', lista_inventario, name='lista_inventario'),
    path('tarjetas/', lista_tarjeta, name='lista_tarjeta'),
    path('favoritos/', lista_favoritos, name='lista_favoritos'),
    path('reclamos/', lista_reclamo, name='lista_reclamo'),
    path('categorias/', lista_categoria, name='lista_categoria'),
    path('productos-categoria/', lista_producto_categoria, name='lista_producto_categoria'),
]
