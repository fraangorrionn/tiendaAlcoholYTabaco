from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('productos/', views.lista_productos, name='lista_productos'),
    path('ordenes/', views.lista_ordenes, name='lista_ordenes'),
    path('detalles-orden/', views.lista_detalles_orden, name='lista_detalles_orden'),
    path('proveedores/', views.lista_proveedores, name='lista_proveedores'),
    path('inventarios/', views.lista_inventarios, name='lista_inventarios'),
    path('tarjetas/', views.lista_tarjetas, name='lista_tarjetas'),
    path('favoritos/', views.lista_favoritos, name='lista_favoritos'),
    path('reclamos/', views.lista_reclamos, name='lista_reclamos'),
    path('categorias/', views.lista_categorias, name='lista_categorias'),
    path('productos-categoria/', views.lista_producto_categoria, name='lista_producto_categoria'),

    path('productos/precio_mayor/<int:precio>/', views.productos_precio_mayor, name='productos_precio_mayor'),  # Parámetero entero
    path('usuarios/favoritos/', views.usuarios_con_productos_favoritos, name='usuarios_con_productos_favoritos'),  # Relación reversa y filtro avanzado
    path('inventarios/bajo_minimo/', views.inventario_bajo_minimo, name='inventario_bajo_minimo'),  # Filtro con None
    path('ordenes/total_aggregado/', views.ordenes_con_total_aggregado, name='ordenes_total_aggregado'),  # Aggregate
    path('productos/categoria/<int:categoria_id>/precio/<int:max_precio>/', views.productos_por_categoria_y_precio, name='productos_por_categoria_y_precio'),  # Dos parámetros
    path('ordenes/recientes/', views.ordenes_recientes, name='ordenes_recientes'),  # Order_by y limit
    path('usuarios/sin_telefono/', views.usuarios_sin_telefono, name='usuarios_sin_telefono'),  # Filtro con None
    path('ordenes/usuario/<int:usuario_id>/', views.detalle_orden_usuario, name='detalle_orden_usuario'),  # ManyToOne
    path('categorias/prioridad/', views.categorias_ordenadas_por_prioridad, name='categorias_ordenadas_por_prioridad'),  # Order_by
    path('productos/buscar/<str:nombre>/', views.buscar_producto, name='buscar_producto'),
    path('productos/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    path('productos/buscar/', views.buscar_productos_por_nombre_o_tipo, name='buscar_productos_por_nombre_o_tipo'),

]