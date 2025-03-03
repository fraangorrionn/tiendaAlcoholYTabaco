from django.urls import path, include
from tienda.api_view import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'productos', ProductoViewSet, basename='productos')

urlpatterns = [
    path('productos/', lista_productos_api, name='lista_productos_api'),
    path('productos/detallados/', lista_productos_detallada_api, name='lista_productos_detallada_api'),
    path('ordenes/', lista_ordenes_api, name='lista_ordenes_api'),
    path('proveedores/', lista_proveedores_api, name='lista_proveedores_api'),
    path('reclamos/', reclamo_list_view, name='reclamo-list'),
    path('usuarios/', lista_usuarios_api, name='lista_usuarios_api'),
    
    
    #----------------------------------------------Formularios---------------------------------------------------------------
    path('productos/busqueda/', busqueda_simple_producto, name='busqueda_simple_producto'),
    path('productos/busqueda-avanzada/', busqueda_avanzada_producto, name='busqueda_avanzada_producto'),
    path('ordenes/busqueda-avanzada/', busqueda_avanzada_orden, name='busqueda_avanzada_orden'),
    path('proveedores/busqueda-avanzada/', busqueda_avanzada_proveedor, name='busqueda_avanzada_proveedor'),
    
    # POST
    path('productos/crear/', crear_producto_api, name='crear_producto_api'),
    path('ordenes/crear/', crear_orden_api, name='crear_orden_api'),
    path('proveedores/crear/', crear_proveedor_api, name='crear_proveedor_api'),
    path('favoritos/crear/', crear_favoritos_api, name='crear_favoritos_api'),
    path('usuarios/crear/', crear_usuario_api, name='crear_usuario_api'),

    
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
    
    # ViewSets
    
    path('', include(router.urls)),
    
    
    #usuario
    path('ordenes/<int:usuario_id>/', obtener_ordenes_usuario, name='obtener_ordenes_usuario'),
    path('registrar/', registrar_usuario.as_view(), name='registrar_usuario'),
    path('usuario/token/<str:token>/', obtener_usuario_token, name='obtener_usuario_token'),

]
