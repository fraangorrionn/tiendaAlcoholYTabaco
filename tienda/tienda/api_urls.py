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
    path('ordenes/crear/', crear_orden_api, name='crear_orden_api'),
    path('proveedores/crear/', crear_proveedor_api, name='crear_proveedor_api'),
    path('favoritos/agregar/', crear_favoritos_api, name='crear_favoritos_api'),
    
    # PUT
    path('productos/<int:producto_id>/editar/', editar_producto_api, name='editar_producto_api'),
    path('ordenes/<int:orden_id>/editar/', editar_orden_api, name='editar_orden_api'),
    path('proveedores/<int:proveedor_id>/editar/', editar_proovedor_api, name='editar_proovedor_api'),
    path('favoritos/<int:favorito_id>/editar/', editar_favoritos_api, name='editar_favoritos_api'),

    # PATCH
    path('productos/<int:producto_id>/actualizar-nombre/', actualizar_nombre_producto_api, name='actualizar_nombre_producto_api'),
    path('ordenes/<int:orden_id>/actualizar-estado/', actualizar_estado_orden_api, name='actualizar_estado_orden_api'),
    path('proveedores/<int:proveedor_id>/actualizar-contacto/', actualizar_contacto_proveedor_api, name='actualizar_contacto_proveedor_api'),
    path('favoritos/<int:favorito_id>/actualizar-prioridad/', actualizar_prioridad_favoritos_api, name='actualizar_prioridad_favoritos_api'),

    # DELETE
    path('productos/<int:producto_id>/eliminar/', eliminar_producto_api, name='eliminar_producto_api'),
    path('ordenes/<int:orden_id>/eliminar/', eliminar_orden_api, name='eliminar_orden_api'),
    path('proveedores/<int:proveedor_id>/eliminar/', eliminar_proveedor_api, name='eliminar_proveedor_api'),
    path('favoritos/<int:favorito_id>/eliminar/', eliminar_favoritos_api, name='eliminar_favoritos_api'),

]
