from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

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
    
    # Formularios - Usuarios
    path('usuarios/crear_usuario/', views.crear_usuario, name='crear_usuario'),
    path('usuarios/leer_usuarios/', views.leer_usuarios, name='leer_usuarios'),
    path('usuarios/editar_usuario/<int:pk>/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/eliminar_usuario/<int:pk>/', views.eliminar_usuario, name='eliminar_usuario'),
    
    # Formularios - Ordenes
    path('ordenes/crear_orden/', views.crear_orden, name='crear_orden'),
    path('ordenes/leer_ordenes/', views.leer_ordenes, name='leer_ordenes'),
    path('ordenes/editar_orden/<int:pk>/', views.editar_orden, name='editar_orden'),
    path('ordenes/eliminar_orden/<int:pk>/', views.eliminar_orden, name='eliminar_orden'),
    
    # Formularios - Proveedores
    path('proveedores/crear_proveedor/', views.crear_proveedor, name='crear_proveedor'),
    path('proveedores/leer_proveedores/', views.leer_proveedores, name='leer_proveedores'),
    path('proveedores/editar_proveedor/<int:pk>/', views.editar_proveedor, name='editar_proveedor'),
    path('proveedores/eliminar_proveedor/<int:pk>/', views.eliminar_proveedor, name='eliminar_proveedor'),
    
    # Formularios - Inventarios
    path('inventarios/crear_inventario/', views.crear_inventario, name='crear_inventario'),
    path('inventarios/leer_inventarios/', views.leer_inventarios, name='leer_inventarios'),
    path('inventarios/editar_inventario/<int:pk>/', views.editar_inventario, name='editar_inventario'),
    path('inventarios/eliminar_inventario/<int:pk>/', views.eliminar_inventario, name='eliminar_inventario'),
    
    # Formularios - Tarjetas
    path('tarjetas/crear_tarjeta/', views.crear_tarjeta, name='crear_tarjeta'),
    path('tarjetas/leer_tarjetas/', views.leer_tarjetas, name='leer_tarjetas'),
    path('tarjetas/editar_tarjeta/<int:pk>/', views.editar_tarjeta, name='editar_tarjeta'),
    path('tarjetas/eliminar_tarjeta/<int:pk>/', views.eliminar_tarjeta, name='eliminar_tarjeta'),
    
    # Formularios - Categorías
    path('categorias/crear_categoria/', views.crear_categoria, name='crear_categoria'),
    path('categorias/leer_categorias/', views.leer_categorias, name='leer_categorias'),
    path('categorias/editar_categoria/<int:pk>/', views.editar_categoria, name='editar_categoria'),
    path('categorias/eliminar_categoria/<int:pk>/', views.eliminar_categoria, name='eliminar_categoria'),

    #Contraseñas y registro
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registro/password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='registro/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registro/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset_done/', auth_views.PasswordResetCompleteView.as_view(template_name='registro/password_reset_complete.html'), name='password_reset_complete'),
    path('registro/', views.registro_usuario, name='registro_usuario'),
    path('login/', auth_views.LoginView.as_view(template_name='registro/login.html'), name='login'),



]

# Configurar manejadores de errores personalizados
handler404 = 'tienda.views.handler_404'
handler500 = 'tienda.views.handler_500'
handler403 = 'tienda.views.handler_403'
handler400 = 'tienda.views.handler_400'
