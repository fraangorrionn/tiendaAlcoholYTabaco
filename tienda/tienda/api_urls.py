from django.urls import path
from tienda.api_view import (
    lista_productos_api, 
    lista_productos_detallada_api, 
    lista_ordenes_api, 
    lista_proveedores_api,
    reclamo_list_view,
    busqueda_simple_producto,
    busqueda_avanzada_producto,
    busqueda_avanzada_orden,
    busqueda_avanzada_proveedor,
)


urlpatterns = [
    path('productos/', lista_productos_api, name='lista_productos_api'),
    path('productos/detallados/', lista_productos_detallada_api, name='lista_productos_detallada_api'),
    path('ordenes/', lista_ordenes_api, name='lista_ordenes_api'),
    path('proveedores/', lista_proveedores_api, name='lista_proveedores_api'),
    path('reclamos/', reclamo_list_view, name='reclamo-list'),
    
    #----------------------------------------------Formularios---------------------------------------------------------------
    path('productos/busqueda/', busqueda_simple_producto, name='busqueda_simple_producto'),
    path('productos/busqueda-avanzada/', busqueda_avanzada_producto, name='busqueda_avanzada_producto'),
    path('ordenes/busqueda-avanzada/', busqueda_avanzada_orden, name='busqueda_avanzada_orden'),
    path('proveedores/busqueda-avanzada/', busqueda_avanzada_proveedor, name='busqueda_avanzada_proveedor'),
]
