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

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('api/productos/', lista_productos_api, name='lista_productos_api'),
    path('api/productos/detallados/', lista_productos_detallada_api, name='lista_productos_detallada_api'),
    path('api/ordenes/', lista_ordenes_api, name='lista_ordenes_api'),
    path('api/proveedores/', lista_proveedores_api, name='lista_proveedores_api'),
    path('api/reclamos/', reclamo_list_view, name='reclamo-list'),

    # Autenticación con JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('api/productos/busqueda/', busqueda_simple_producto, name='busqueda_simple_producto'),
    path('api/productos/busqueda-avanzada/', busqueda_avanzada_producto, name='busqueda_avanzada_producto'),
    path('api/ordenes/busqueda-avanzada/', busqueda_avanzada_orden, name='busqueda_avanzada_orden'),
    path('api/proveedores/busqueda-avanzada/', busqueda_avanzada_proveedor, name='busqueda_avanzada_proveedor'),
]
