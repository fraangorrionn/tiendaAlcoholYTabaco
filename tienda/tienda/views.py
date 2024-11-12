from django.db.models import Q, Count, Sum, F , Prefetch
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from .models import Usuario, Producto, Orden, DetalleOrden, Provedor, Inventario, Tarjeta, Favoritos, Reclamo, Categoria, ProductoCategoria

# Vista principal que redirige al índice de URLs.
def index(request):
    return render(request, 'index.html')

# Muestra una lista de todos los usuarios registrados en la plataforma con su tarjeta y productos favoritos.
def lista_usuarios(request):
    usuarios = Usuario.objects.select_related('tarjeta').prefetch_related('productos_favoritos').all()
    return render(request, 'usuario/lista_usuarios.html', {'usuarios': usuarios})

# Muestra una lista de todos los productos con sus categorías, ordenados por precio.
def lista_productos(request):
    productos = Producto.objects.prefetch_related('categorias').order_by('-precio')
    return render(request, 'productos/lista_productos.html', {'productos': productos})

# Lista todas las órdenes con el usuario asociado, mostrando las últimas 10 órdenes.
def lista_ordenes(request):
    ordenes = Orden.objects.select_related('usuario').order_by('-fecha_orden')[:10]
    return render(request, 'ordenes/lista_ordenes.html', {'ordenes': ordenes})

# Lista todos los detalles de las órdenes, incluyendo subtotal para cada producto.
def lista_detalles_orden(request):
    detalles = DetalleOrden.objects.all()
    
    # Calculamos el subtotal para cada detalle
    for detalle in detalles:
        detalle.subtotal = detalle.cantidad * detalle.precio_unitario - detalle.descuento_aplicado
    
    return render(request, 'detalles_orden/lista_detalles_orden.html', {'detalles': detalles})

# Lista todos los proveedores y los productos que suministran.
def lista_proveedores(request):
    proveedores = Provedor.objects.prefetch_related('productos')
    return render(request, 'proveedores/lista_proveedores.html', {'proveedores': proveedores})

# Muestra el inventario de productos ordenado por cantidad disponible, mostrando productos con inventario bajo el mínimo.
def lista_inventarios(request):
    inventarios = Inventario.objects.select_related('producto').filter(cantidad_disponible__lt=F('minimo_requerido')).order_by('cantidad_disponible')
    return render(request, 'inventarios/lista_inventarios.html', {'inventarios': inventarios})

# Lista todas las tarjetas asociadas a los usuarios, mostrando solo las tarjetas con fecha de expiración futura.
def lista_tarjetas(request):
    tarjetas = Tarjeta.objects.select_related('usuario').all()
    context = {
        'tarjetas': tarjetas,
        'today': timezone.now().date()  # Fecha actual para validar si la tarjeta está expirada
    }
    return render(request, 'tarjetas/lista_tarjetas.html', context)

# Muestra los productos favoritos de cada usuario, solo los favoritos de alta prioridad.
def lista_favoritos(request):
    favoritos = Favoritos.objects.select_related('usuario', 'producto').filter(prioridad__gte=2)
    return render(request, 'favoritos/lista_favoritos.html', {'favoritos': favoritos})

# Lista los reclamos realizados, con opción de filtrar solo los pendientes.
def lista_reclamos(request):
    mostrar_pendientes = request.GET.get('pendientes', 'false') == 'true'
    
    if mostrar_pendientes:
        reclamos = Reclamo.objects.select_related('usuario', 'detalle_orden').filter(respuesta__isnull=True)
    else:
        reclamos = Reclamo.objects.select_related('usuario', 'detalle_orden')
        
    return render(request, 'reclamos/lista_reclamos.html', {'reclamos': reclamos, 'mostrar_pendientes': mostrar_pendientes})

# Muestra las categorías activas, ordenadas por prioridad.
def lista_categorias(request):
    categorias = Categoria.objects.filter(estado='activo').order_by('-prioridad')
    return render(request, 'categoria/lista_categorias.html', {'categorias': categorias})

# Muestra la relación entre productos y categorías, filtrando categorías activas.
def lista_producto_categoria(request):
    productos_categoria = ProductoCategoria.objects.select_related('producto', 'categoria').filter(categoria__estado='activo')
    return render(request, 'producto_categoria/lista_producto_categoria.html', {'productos_categoria': productos_categoria})

# Muestra productos con precio mayor al valor especificado.
def productos_precio_mayor(request, precio):
    productos = Producto.objects.filter(precio__gt=precio)
    return render(request, 'productos/precio_mayor.html', {'productos': productos})

# Lista usuarios que tienen múltiples productos favoritos en diferentes categorías.
def usuarios_con_productos_favoritos(request):
    usuarios = Usuario.objects.annotate(num_favoritos=Count('productos_favoritos')).filter(num_favoritos__gt=1)
    return render(request, 'usuario/usuarios_con_productos_favoritos.html', {'usuarios': usuarios})

# Muestra productos cuyo inventario está por debajo del mínimo requerido.
def inventario_bajo_minimo(request):
    inventarios = Inventario.objects.filter(cantidad_disponible__lt=F('minimo_requerido'))
    return render(request, 'inventarios/inventario_bajo_minimo.html', {'inventarios': inventarios})

# Muestra la suma total de todas las órdenes.
def ordenes_con_total_aggregado(request):
    total_ordenes = Orden.objects.aggregate(total=Sum('total'))
    return render(request, 'ordenes/total_aggregado.html', {'total_ordenes': total_ordenes})

# Muestra productos de una categoría específica y con precio menor a max_precio.
def productos_por_categoria_y_precio(request, categoria_id, max_precio):
    productos = Producto.objects.filter(categorias__id=categoria_id, precio__lt=max_precio)
    return render(request, 'productos/por_categoria_y_precio.html', {'productos': productos})

# Muestra las últimas 5 órdenes ordenadas por fecha.
def ordenes_recientes(request):
    ordenes = Orden.objects.order_by('-fecha_orden')[:5]
    return render(request, 'ordenes/ordenes_recientes.html', {'ordenes': ordenes})

# Muestra usuarios que no tienen teléfono registrado (campo None).
def usuarios_sin_telefono(request):
    usuarios = Usuario.objects.filter(telefono__isnull=True)
    return render(request, 'usuario/usuarios_sin_telefono.html', {'usuarios': usuarios})

# Muestra las órdenes de un usuario específico, incluyendo detalles de cada orden.
def detalle_orden_usuario(request, usuario_id):
    ordenes_usuario = Orden.objects.filter(usuario_id=usuario_id).select_related('usuario').prefetch_related('detalleorden_set__producto')
    
    # Calcular el subtotal para cada detalle de orden
    for orden in ordenes_usuario:
        for detalle in orden.detalleorden_set.all():
            detalle.subtotal = detalle.cantidad * detalle.precio_unitario - detalle.descuento_aplicado
    
    return render(request, 'ordenes/detalle_orden_usuario.html', {'ordenes_usuario': ordenes_usuario})

# Muestra categorías ordenadas por prioridad de mayor a menor.
def categorias_ordenadas_por_prioridad(request):
    categorias = Categoria.objects.order_by('-prioridad')
    return render(request, 'categoria/categorias_prioridad.html', {'categorias': categorias})

# Muestra detalles de un producto específico por ID.
def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'productos/detalle_producto.html', {'producto': producto})

# Busca productos por nombre.
def buscar_producto(request, nombre):
    productos = Producto.objects.filter(nombre__icontains=nombre)
    return render(request, 'productos/buscar_producto.html', {'productos': productos})

# Busca productos por nombre o tipo.
def buscar_productos_por_nombre_o_tipo(request):
    query = request.GET.get('q')
    
    if not query:  # Verifica si 'query' es None o está vacío
        productos = Producto.objects.none()  # Retorna un queryset vacío si no hay valor de búsqueda
    else:
        productos = Producto.objects.filter(Q(nombre__icontains=query) | Q(tipo__icontains=query))
    
    return render(request, 'productos/buscar_productos.html', {'productos': productos})

# Errores
def handler_404(request, exception):
    """Muestra una página personalizada para el error 404 (página no encontrada)."""
    return render(request, '404.html', status=404)

def handler_500(request):
    """Muestra una página personalizada para el error 500 (error interno del servidor)."""
    return render(request, '500.html', status=500)

def handler_403(request, exception):
    """Muestra una página personalizada para el error 403 (prohibido)."""
    return render(request, '403.html', status=403)

def handler_400(request, exception):
    """Muestra una página personalizada para el error 400 (solicitud incorrecta)."""
    return render(request, '400.html', status=400)