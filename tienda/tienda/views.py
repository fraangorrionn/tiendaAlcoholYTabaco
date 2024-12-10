from django.db.models import Q, Count, Sum, F , Prefetch
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from .models import Usuario, Producto, Orden, DetalleOrden, Provedor, Inventario, Tarjeta, Favoritos, Reclamo, Categoria, ProductoCategoria
from .forms import *

# Vista principal que redirige al índice de URLs.
def index(request):
    return render(request, 'index.html')

# Muestra una lista de todos los usuarios registrados en la plataforma con su tarjeta y productos favoritos.
def lista_usuarios(request):
    usuarios = Usuario.objects.select_related('tarjeta').prefetch_related('productos_favoritos').all()
    return render(request, 'Paginas/usuarios_list.html', {'usuarios': usuarios})

# Muestra una lista de todos los productos con sus categorías, ordenados por precio.
def lista_productos(request):
    productos = Producto.objects.prefetch_related('categorias').order_by('-precio')
    return render(request, 'Paginas/productos_list.html', {'productos': productos})

# Lista todas las órdenes con el usuario asociado, mostrando las últimas 10 órdenes.
def lista_ordenes(request):
    ordenes = Orden.objects.select_related('usuario').order_by('-fecha_orden')[:10]
    return render(request, 'Paginas/ordenes_list.html', {'ordenes': ordenes})

# Lista todos los detalles de las órdenes, incluyendo subtotal para cada producto.
def lista_detalles_orden(request):
    # Usamos select_related para optimizar la carga de los productos y las órdenes relacionadas
    detalles = DetalleOrden.objects.select_related('producto', 'orden').all()

    # Calculamos el subtotal para cada detalle
    for detalle in detalles:
        detalle.subtotal = detalle.cantidad * detalle.precio_unitario - detalle.descuento_aplicado
    
    return render(request, 'Paginas/detalles_orden_list.html', {'detalles': detalles})

# Lista todos los proveedores y los productos que suministran.
def lista_proveedores(request):
    proveedores = Provedor.objects.prefetch_related('productos')
    return render(request, 'Paginas/proveedor_list.html', {'proveedores': proveedores})

# Muestra el inventario de productos ordenado por cantidad disponible, mostrando productos con inventario bajo el mínimo.
def lista_inventarios(request):
    inventarios = Inventario.objects.select_related('producto').filter(cantidad_disponible__lt=F('minimo_requerido')).order_by('cantidad_disponible')
    return render(request, 'Paginas/inventarios_list.html', {'inventarios': inventarios})

# Lista todas las tarjetas asociadas a los usuarios, mostrando solo las tarjetas con fecha de expiración futura.
def lista_tarjetas(request):
    tarjetas = Tarjeta.objects.select_related('usuario').all()
    context = {
        'tarjetas': tarjetas,
        'today': timezone.now().date()  # Fecha actual para validar si la tarjeta está expirada
    }
    return render(request, 'Paginas/tarjetas_list.html', context)

# Muestra los productos favoritos de cada usuario, solo los favoritos de alta prioridad.
def lista_favoritos(request):
    favoritos = Favoritos.objects.select_related('usuario', 'producto').filter(prioridad__gte=2)
    return render(request, 'Paginas/favoritos_list.html', {'favoritos': favoritos})

# Lista los reclamos realizados, con opción de filtrar solo los pendientes.
def lista_reclamos(request):
    mostrar_pendientes = request.GET.get('pendientes', 'false') == 'true'
    
    if mostrar_pendientes:
        reclamos = Reclamo.objects.select_related('usuario', 'detalle_orden').filter(respuesta__isnull=True)
    else:
        reclamos = Reclamo.objects.select_related('usuario', 'detalle_orden')
        
    return render(request, 'Paginas/reclamos_list.html', {'reclamos': reclamos, 'mostrar_pendientes': mostrar_pendientes})

# Muestra las categorías activas, ordenadas por prioridad.
def lista_categorias(request):
    categorias = Categoria.objects.filter(estado='activo').order_by('-prioridad')
    return render(request, 'Paginas/categorias_list.html', {'categorias': categorias})

# Muestra la relación entre productos y categorías, filtrando categorías activas.
def lista_producto_categoria(request):
    # Filtrar relaciones donde 'nota_adicional' sea None o esté vacío
    productos_categoria = ProductoCategoria.objects.select_related('producto', 'categoria').filter(
        Q(nota_adicional__isnull=True) | Q(nota_adicional=""),
        categoria__estado='activo'  # Mantener el filtro por estado activo
    )

    return render(request, 'Paginas/producto_categoria_list.html', {'productos_categoria': productos_categoria})

# Muestra productos con precio mayor al valor especificado.
def productos_precio_mayor(request, precio):
    productos = Producto.objects.filter(precio__gt=precio)
    return render(request, 'Paginas/precio_mayor_list.html', {'productos': productos})

# Lista usuarios que tienen múltiples productos favoritos en diferentes categorías.
def usuarios_con_productos_favoritos(request):
    usuarios = Usuario.objects.annotate(num_favoritos=Count('productos_favoritos')).filter(num_favoritos__gt=1)
    return render(request, 'Paginas/usuarios_con_productos_favoritos_list.html', {'usuarios': usuarios})

# Muestra productos cuyo inventario está por debajo del mínimo requerido.
def inventario_bajo_minimo(request):
    # Usamos select_related para optimizar la consulta y cargar los productos de una vez
    inventarios = Inventario.objects.select_related('producto').filter(cantidad_disponible__lt=F('minimo_requerido'))
    return render(request, 'Paginas/inventario_bajo_minimo_list.html', {'inventarios': inventarios})

# Muestra la suma total de todas las órdenes.
def ordenes_con_total_aggregado(request):
    total_ordenes = Orden.objects.aggregate(total=Sum('total'))
    return render(request, 'Paginas/total_aggregado_list.html', {'total_ordenes': total_ordenes})

# Muestra productos de una categoría específica y con precio menor a max_precio.
def productos_por_categoria_y_precio(request, categoria_id, max_precio):
    productos = Producto.objects.filter(categorias__id=categoria_id, precio__lt=max_precio)
    return render(request, 'Paginas/por_categoria_y_precio_list.html', {'productos': productos})

# Muestra las últimas 5 órdenes ordenadas por fecha.
def ordenes_recientes(request):
    # Usamos select_related para optimizar la consulta y obtener el usuario asociado a las órdenes
    ordenes = Orden.objects.select_related('usuario').order_by('-fecha_orden')[:5]
    return render(request, 'Paginas/ordenes_recientes_list.html', {'ordenes': ordenes})

# Muestra usuarios que no tienen teléfono registrado (campo None).
def usuarios_sin_telefono(request):
    usuarios = Usuario.objects.filter(telefono__isnull=True)
    return render(request, 'Paginas/usuarios_sin_telefono_list.html', {'usuarios': usuarios})

# Muestra las órdenes de un usuario específico, incluyendo detalles de cada orden.
def detalle_orden_usuario(request, usuario_id):
    # Usa select_related para optimizar la carga del usuario y prefetch_related para los productos relacionados con los detalles de las órdenes
    ordenes_usuario = Orden.objects.filter(usuario_id=usuario_id).select_related('usuario').prefetch_related('detalleorden_set__producto')

    # Si quieres calcular el subtotal en la vista antes de pasarlo al template, lo puedes hacer de la siguiente manera
    for orden in ordenes_usuario:
        for detalle in orden.detalleorden_set.all():
            detalle.subtotal_calculado = detalle.subtotal()  # Usamos el método subtotal que definimos en el modelo

    return render(request, 'Paginas/detalle_orden_usuario_list.html', {'ordenes_usuario': ordenes_usuario})

# Muestra categorías ordenadas por prioridad de mayor a menor.
def categorias_ordenadas_por_prioridad(request):
    categorias = Categoria.objects.order_by('-prioridad')
    return render(request, 'Paginas/categorias_prioridad_list.html', {'categorias': categorias})

# Muestra detalles de un producto específico por ID.
def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'Paginas/detalle_producto_list.html', {'producto': producto})

# Busca productos por nombre.
def buscar_producto(request, nombre):
    productos = Producto.objects.filter(nombre__icontains=nombre)
    return render(request, 'Paginas/buscar_producto_list.html', {'productos': productos})

# Busca productos por nombre o tipo.
def buscar_productos_por_nombre_o_tipo(request):
    # Obtener la consulta de la URL
    query = request.GET.get('q', '').strip()  # Asegúrate de manejar espacios en blanco
    
    if query:  # Si 'query' tiene un valor
        # Filtra productos por nombre o tipo
        productos = Producto.objects.filter(Q(nombre__icontains=query) | Q(tipo__icontains=query))
    else:
        # Retorna un queryset vacío si no hay búsqueda
        productos = Producto.objects.none()
    
    return render(request, 'Paginas/por_nombre_o_tipo_list.html', {'productos': productos, 'query': query})

#Formularios

# Crear un nuevo usuario
def crear_usuario(request):
    formulario = UsuarioModelForm(request.POST or None)
    if request.method == "POST":
        if formulario.is_valid():
            formulario.save()
            return redirect("lista_usuarios")  # Redirige a la lista de usuarios
    return render(request, 'formularios/crear_usuario.html', {"formulario": formulario})

# Leer la lista de usuarios
def leer_usuarios(request):
    # Obtén todos los usuarios inicialmente
    usuarios = Usuario.objects.all()

    # Obtener valores del formulario GET
    nombre = request.GET.get('nombre', '')
    tipo_usuario = request.GET.get('tipo_usuario', '')
    direccion = request.GET.get('direccion', '')

    # Filtrar usuarios según los criterios
    if nombre:
        usuarios = usuarios.filter(nombre__icontains=nombre)
    if tipo_usuario:
        usuarios = usuarios.filter(tipo_usuario=tipo_usuario)
    if direccion:
        usuarios = usuarios.filter(direccion__icontains=direccion)

    return render(request, 'formularios/leer_usuarios.html', {
        "usuarios": usuarios,
        "filtros": {
            "nombre": nombre,
            "tipo_usuario": tipo_usuario,
            "direccion": direccion,
        }
    })

# Actualizar un usuario existente
def editar_usuario(request, pk):
    try:
        usuario = Usuario.objects.get(pk=pk)  # Manejo manual de consulta
    except Usuario.DoesNotExist:
        return render(request, '404.html', status=404)  # Mostrar error 404 si no se encuentra

    formulario = UsuarioModelForm(request.POST or None, instance=usuario)
    if request.method == "POST":
        if formulario.is_valid():
            formulario.save()
            return redirect("lista_usuarios")
    return render(request, 'formularios/editar_usuario.html', {"formulario": formulario, "usuario": usuario})

# Eliminar un usuario
def eliminar_usuario(request, pk):
    try:
        usuario = Usuario.objects.get(pk=pk)
    except Usuario.DoesNotExist:
        return render(request, '404.html', status=404)

    if request.method == "POST":
        usuario.delete()
        return redirect("lista_usuarios")
    return render(request, 'formularios/eliminar_usuario.html', {"usuario": usuario})

def crear_orden(request):
    formulario = OrdenModelForm(request.POST or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('lista_ordenes')
    return render(request, 'formularios/crear_orden.html', {'formulario': formulario})

def leer_ordenes(request):
    ordenes = Orden.objects.select_related('usuario').all()

    # Obtener valores del formulario
    estado = request.GET.get('estado', '')
    usuario = request.GET.get('usuario', '')
    total_min = request.GET.get('total_min', None)
    total_max = request.GET.get('total_max', None)

    # Aplicar filtros
    if estado:
        ordenes = ordenes.filter(estado=estado)
    if usuario:
        ordenes = ordenes.filter(usuario__id=usuario)
    if total_min:
        ordenes = ordenes.filter(total__gte=total_min)
    if total_max:
        ordenes = ordenes.filter(total__lte=total_max)

    # Obtener usuarios para el formulario
    usuarios = Usuario.objects.all()

    return render(request, 'formularios/leer_ordenes.html', {
        "ordenes": ordenes,
        "usuarios": usuarios,
        "filtros": {
            "estado": estado,
            "usuario": usuario,
            "total_min": total_min,
            "total_max": total_max,
        }
    })

def editar_orden(request, pk):
    orden = get_object_or_404(Orden, pk=pk)
    formulario = OrdenModelForm(request.POST or None, instance=orden)
    if formulario.is_valid():
        formulario.save()
        return redirect('lista_ordenes')
    return render(request, 'formularios/editar_orden.html', {'formulario': formulario, 'orden': orden})

def eliminar_orden(request, pk):
    orden = get_object_or_404(Orden, pk=pk)
    if request.method == 'POST':
        orden.delete()
        return redirect('lista_ordenes')
    return render(request, 'formularios/eliminar_orden.html', {'orden': orden})

def crear_provedor(request):
    formulario = ProvedorModelForm(request.POST or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('lista_proveedores')
    return render(request, 'formularios/crear_provedor.html', {'formulario': formulario})

def leer_provedores(request):
    provedores = Provedor.objects.all()

    # Obtener valores de los filtros del formulario
    nombre = request.GET.get('nombre', '')
    contacto = request.GET.get('contacto', '')
    telefono = request.GET.get('telefono', '')

    # Aplicar filtros
    if nombre:
        provedores = provedores.filter(nombre__icontains=nombre)
    if contacto:
        provedores = provedores.filter(contacto__icontains=contacto)
    if telefono:
        provedores = provedores.filter(telefono__icontains=telefono)

    return render(request, 'formularios/leer_proveedores.html', {
        "provedores": provedores,
        "filtros": {
            "nombre": nombre,
            "contacto": contacto,
            "telefono": telefono,
        }
    })


def editar_provedor(request, pk):
    provedor = get_object_or_404(Provedor, pk=pk)
    formulario = ProvedorModelForm(request.POST or None, instance=provedor)
    if formulario.is_valid():
        formulario.save()
        return redirect('lista_proveedores')
    return render(request, 'formularios/editar_provedor.html', {'formulario': formulario, 'provedor': provedor})

def eliminar_provedor(request, pk):
    provedor = get_object_or_404(Provedor, pk=pk)
    if request.method == 'POST':
        provedor.delete()
        return redirect('lista_proveedores')
    return render(request, 'formularios/eliminar_provedor.html', {'provedor': provedor})

def crear_inventario(request):
    formulario = InventarioModelForm(request.POST or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('lista_inventarios')
    return render(request, 'formularios/crear_inventario.html', {'formulario': formulario})

def leer_inventarios(request):
    inventarios = Inventario.objects.select_related('producto').all()

    # Obtener valores de los filtros del formulario
    producto = request.GET.get('producto', '')
    ubicacion = request.GET.get('ubicacion', '')
    cantidad_min = request.GET.get('cantidad_min', None)
    cantidad_max = request.GET.get('cantidad_max', None)

    # Aplicar filtros
    if producto:
        inventarios = inventarios.filter(producto__nombre__icontains=producto)
    if ubicacion:
        inventarios = inventarios.filter(ubicacion__icontains=ubicacion)
    if cantidad_min:
        inventarios = inventarios.filter(cantidad_disponible__gte=cantidad_min)
    if cantidad_max:
        inventarios = inventarios.filter(cantidad_disponible__lte=cantidad_max)

    return render(request, 'formularios/leer_inventarios.html', {
        "inventarios": inventarios,
        "filtros": {
            "producto": producto,
            "ubicacion": ubicacion,
            "cantidad_min": cantidad_min,
            "cantidad_max": cantidad_max,
        }
    })


def editar_inventario(request, pk):
    inventario = get_object_or_404(Inventario, pk=pk)
    formulario = InventarioModelForm(request.POST or None, instance=inventario)
    if formulario.is_valid():
        formulario.save()
        return redirect('lista_inventarios')
    return render(request, 'formularios/editar_inventario.html', {'formulario': formulario, 'inventario': inventario})

def eliminar_inventario(request, pk):
    inventario = get_object_or_404(Inventario, pk=pk)
    if request.method == 'POST':
        inventario.delete()
        return redirect('lista_inventarios')
    return render(request, 'formularios/eliminar_inventario.html', {'inventario': inventario})

def crear_tarjeta(request):
    formulario = TarjetaModelForm(request.POST or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('lista_tarjetas')
    return render(request, 'formularios/crear_tarjeta.html', {'formulario': formulario})

def leer_tarjetas(request):
    tarjetas = Tarjeta.objects.select_related('usuario').all()

    # Obtener valores de los filtros del formulario
    usuario = request.GET.get('usuario', '')
    tipo = request.GET.get('tipo', '')
    fecha_inicio = request.GET.get('fecha_inicio', None)
    fecha_fin = request.GET.get('fecha_fin', None)

    # Aplicar filtros
    if usuario:
        tarjetas = tarjetas.filter(usuario__nombre__icontains=usuario)
    if tipo:
        tarjetas = tarjetas.filter(tipo__icontains=tipo)
    if fecha_inicio:
        tarjetas = tarjetas.filter(fecha_expiracion__gte=fecha_inicio)
    if fecha_fin:
        tarjetas = tarjetas.filter(fecha_expiracion__lte=fecha_fin)

    return render(request, 'formularios/leer_tarjetas.html', {
        "tarjetas": tarjetas,
        "filtros": {
            "usuario": usuario,
            "tipo": tipo,
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
        }
    })

def editar_tarjeta(request, pk):
    tarjeta = get_object_or_404(Tarjeta, pk=pk)
    formulario = TarjetaModelForm(request.POST or None, instance=tarjeta)
    if formulario.is_valid():
        formulario.save()
        return redirect('lista_tarjetas')
    return render(request, 'formularios/editar_tarjeta.html', {'formulario': formulario, 'tarjeta': tarjeta})

def eliminar_tarjeta(request, pk):
    tarjeta = get_object_or_404(Tarjeta, pk=pk)
    if request.method == 'POST':
        tarjeta.delete()
        return redirect('lista_tarjetas')
    return render(request, 'formularios/eliminar_tarjeta.html', {'tarjeta': tarjeta})

# Crear categoría
def crear_categoria(request):
    formulario = CategoriaModelForm(request.POST or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('leer_categorias')
    return render(request, 'formularios/crear_categoria.html', {'formulario': formulario})

# Leer categorías
def leer_categorias(request):
    categorias = Categoria.objects.all()

    # Filtros de búsqueda
    nombre = request.GET.get('nombre', '')
    estado = request.GET.get('estado', '')
    prioridad_min = request.GET.get('prioridad_min', None)
    prioridad_max = request.GET.get('prioridad_max', None)

    # Aplicar filtros si están presentes
    if nombre:
        categorias = categorias.filter(nombre__icontains=nombre)
    if estado:
        categorias = categorias.filter(estado=estado)
    if prioridad_min:
        categorias = categorias.filter(prioridad__gte=prioridad_min)
    if prioridad_max:
        categorias = categorias.filter(prioridad__lte=prioridad_max)

    return render(request, 'formularios/leer_categorias.html', {
        'categorias': categorias,
        'filtros': {
            'nombre': nombre,
            'estado': estado,
            'prioridad_min': prioridad_min,
            'prioridad_max': prioridad_max,
        }
    })


# Editar categoría
def editar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    formulario = CategoriaModelForm(request.POST or None, instance=categoria)
    if formulario.is_valid():
        formulario.save()
        return redirect('leer_categorias')
    return render(request, 'formularios/editar_categoria.html', {'formulario': formulario, 'categoria': categoria})

# Eliminar categoría
def eliminar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        return redirect('leer_categorias')
    return render(request, 'formularios/eliminar_categoria.html', {'categoria': categoria})

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