from django.urls import path
from tienda.api_view import *


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
    
    # POST
    path('productos/crear/', crear_producto_api, name='crear_producto_api'),
    
    # PUT
    path('productos/<int:producto_id>/actualizar/', actualizar_producto_api, name='actualizar_producto_api'),
    
    # PATCH
    path('productos/<int:producto_id>/actualizar-nombre/', actualizar_nombre_producto_api, name='actualizar_nombre_producto_api'),
    
    # DELETE
    path('productos/<int:producto_id>/eliminar/', eliminar_producto_api, name='eliminar_producto_api'),

]
