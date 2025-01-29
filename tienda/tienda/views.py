from django.db.models import Q, Count, Sum, F , Prefetch
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from .models import Usuario, Producto, Orden, DetalleOrden, Provedor, Inventario, Tarjeta, Favoritos, Reclamo, Categoria, ProductoCategoria
from .forms import *
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Group
from django.contrib.auth import logout
from django.utils.timezone import now
from django.contrib.auth.models import Permission


def index(request):
    # Establecer la fecha de inicio de sesión
    if not "fecha_inicio" in request.session:
        request.session["fecha_inicio"] = now().strftime('%d/%m/%Y %H:%M')

    # Variables de sesión adicionales
    if request.user.is_authenticated:
        request.session["nombre_usuario"] = request.user.username  # Nombre del usuario logueado
        request.session["rol"] = request.user.get_rol_display()  # Usar el método para mostrar el rol legible
        request.session["productos_favoritos"] = Favoritos.objects.filter(usuario=request.user).count()
    else:
        request.session["nombre_usuario"] = "Visitante"
        request.session["rol"] = "N/A"
        request.session["productos_favoritos"] = 0

    return render(request, 'index.html')

# LISTA DE USUARIOS
@permission_required('tienda.view_usuario')
def lista_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'Paginas/usuarios_list.html', {'usuarios': usuarios})

# LISTA DE PRODUCTOS
@permission_required('tienda.view_producto')
def lista_productos(request):
    productos = Producto.objects.prefetch_related('categorias').order_by('-precio')
    return render(request, 'Paginas/productos_list.html', {'productos': productos})

# LISTA DE ÓRDENES
@permission_required('tienda.view_orden')
def lista_ordenes(request):
    if request.user.rol == Usuario.CLIENTE:
        ordenes = Orden.objects.filter(usuario=request.user).select_related('usuario').order_by('-fecha_orden')[:10]
    else:
        ordenes = Orden.objects.select_related('usuario').order_by('-fecha_orden')[:10]

    return render(request, 'Paginas/ordenes_list.html', {'ordenes': ordenes})

# LISTA DE DETALLES DE ÓRDENES
@permission_required('tienda.view_detalleorden')
def lista_detalles_orden(request):
    detalles = DetalleOrden.objects.select_related('producto', 'orden').all()
    for detalle in detalles:
        detalle.subtotal = detalle.cantidad * detalle.precio_unitario - detalle.descuento_aplicado

    return render(request, 'Paginas/detalles_orden_list.html', {'detalles': detalles})

# LISTA DE PROVEEDORES
@permission_required('tienda.view_provedor')
def lista_proveedores(request):
    proveedores = Provedor.objects.prefetch_related('productos')
    return render(request, 'Paginas/proveedor_list.html', {'proveedores': proveedores})

# LISTA DE INVENTARIOS
@permission_required('tienda.view_inventario')
def lista_inventarios(request):
    inventarios = Inventario.objects.select_related('producto').filter(cantidad_disponible__lt=F('minimo_requerido')).order_by('cantidad_disponible')
    return render(request, 'Paginas/inventarios_list.html', {'inventarios': inventarios})

# LISTA DE TARJETAS
@permission_required('tienda.view_tarjeta')
def lista_tarjetas(request):
    tarjetas = Tarjeta.objects.select_related('usuario').all()
    context = {
        'tarjetas': tarjetas,
        'today': timezone.now().date()
    }
    return render(request, 'Paginas/tarjetas_list.html', context)

# LISTA DE FAVORITOS
@permission_required('tienda.view_favoritos')
def lista_favoritos(request):
    favoritos = Favoritos.objects.select_related('usuario', 'producto').filter(prioridad__gte=2)
    return render(request, 'Paginas/favoritos_list.html', {'favoritos': favoritos})

# LISTA DE RECLAMOS
@permission_required('tienda.view_reclamo')
def lista_reclamos(request):
    mostrar_pendientes = request.GET.get('pendientes', 'false') == 'true'

    if mostrar_pendientes:
        reclamos = Reclamo.objects.select_related('usuario', 'detalle_orden').filter(respuesta__isnull=True)
    else:
        reclamos = Reclamo.objects.select_related('usuario', 'detalle_orden')

    return render(request, 'Paginas/reclamos_list.html', {'reclamos': reclamos, 'mostrar_pendientes': mostrar_pendientes})

# LISTA DE CATEGORÍAS
@permission_required('tienda.view_categoria')
def lista_categorias(request):
    categorias = Categoria.objects.filter(estado='activo').order_by('-prioridad')
    return render(request, 'Paginas/categorias_list.html', {'categorias': categorias})

# LISTA DE PRODUCTOS POR CATEGORÍA
@permission_required('tienda.view_productocategoria')
def lista_producto_categoria(request):
    productos_categoria = ProductoCategoria.objects.select_related('producto', 'categoria').filter(
        Q(nota_adicional__isnull=True) | Q(nota_adicional=""),
        categoria__estado='activo'
    )
    return render(request, 'Paginas/producto_categoria_list.html', {'productos_categoria': productos_categoria})



def productos_precio_mayor(request, precio):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')

    productos = Producto.objects.filter(precio__gt=precio)
    return render(request, 'Paginas/precio_mayor_list.html', {'productos': productos})

def usuarios_con_productos_favoritos(request):
    if not request.user.is_authenticated or request.user.rol != Usuario.ADMINISTRADOR:
        return redirect('/accounts/login/')

    usuarios = Usuario.objects.annotate(num_favoritos=Count('productos_favoritos')).filter(num_favoritos__gt=1)
    return render(request, 'Paginas/usuarios_con_productos_favoritos_list.html', {'usuarios': usuarios})

def inventario_bajo_minimo(request):
    if not request.user.is_authenticated or request.user.rol != Usuario.GERENTE:
        return redirect('/accounts/login/')

    inventarios = Inventario.objects.select_related('producto').filter(cantidad_disponible__lt=F('minimo_requerido'))
    return render(request, 'Paginas/inventario_bajo_minimo_list.html', {'inventarios': inventarios})

def ordenes_con_total_aggregado(request):
    if not request.user.is_authenticated or request.user.rol != Usuario.ADMINISTRADOR:
        return redirect('/accounts/login/')

    total_ordenes = Orden.objects.aggregate(total=Sum('total'))
    return render(request, 'Paginas/total_aggregado_list.html', {'total_ordenes': total_ordenes})

def productos_por_categoria_y_precio(request, categoria_id, max_precio):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')

    productos = Producto.objects.filter(categorias__id=categoria_id, precio__lt=max_precio)
    return render(request, 'Paginas/por_categoria_y_precio_list.html', {'productos': productos})

@permission_required('tienda.view_orden')
def ordenes_recientes(request):
    ordenes = Orden.objects.select_related('usuario').order_by('-fecha_orden')[:5]
    return render(request, 'Paginas/ordenes_recientes_list.html', {'ordenes': ordenes})

def usuarios_sin_telefono(request):
    if not request.user.is_authenticated or request.user.rol != Usuario.ADMINISTRADOR:
        return redirect('/accounts/login/')

    usuarios = Usuario.objects.filter(telefono__isnull=True)
    return render(request, 'Paginas/usuarios_sin_telefono_list.html', {'usuarios': usuarios})

def detalle_orden_usuario(request, usuario_id):
    if not request.user.is_authenticated or request.user.rol != Usuario.ADMINISTRADOR:
        return redirect('/accounts/login/')

    ordenes_usuario = Orden.objects.filter(usuario_id=usuario_id).select_related('usuario').prefetch_related('detalleorden_set__producto')

    for orden in ordenes_usuario:
        for detalle in orden.detalleorden_set.all():
            detalle.subtotal_calculado = detalle.subtotal()

    return render(request, 'Paginas/detalle_orden_usuario_list.html', {'ordenes_usuario': ordenes_usuario})

def categorias_ordenadas_por_prioridad(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')

    categorias = Categoria.objects.order_by('-prioridad')
    return render(request, 'Paginas/categorias_prioridad_list.html', {'categorias': categorias})

def detalle_producto(request, producto_id):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')

    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'Paginas/detalle_producto_list.html', {'producto': producto})

def buscar_producto(request, nombre):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')

    productos = Producto.objects.filter(nombre__icontains=nombre)
    return render(request, 'Paginas/buscar_producto_list.html', {'productos': productos})

def buscar_productos_por_nombre_o_tipo(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')

    query = request.GET.get('q', '').strip()

    if query:
        productos = Producto.objects.filter(Q(nombre__icontains=query) | Q(tipo__icontains=query))
    else:
        productos = Producto.objects.none()

    return render(request, 'Paginas/por_nombre_o_tipo_list.html', {'productos': productos, 'query': query})


#Formularios

# Crear un nuevo usuario

# CRUD para Usuarios
@permission_required('tienda.add_usuario')
def crear_usuario(request):
    formulario = UsuarioModelForm(request.POST or None)
    if formulario.is_valid():
        formulario.save()
        return redirect("lista_usuarios")
    return render(request, 'formularios/crear_usuario.html', {"formulario": formulario})

@permission_required('tienda.view_usuario')
def leer_usuarios(request):
    formulario = BusquedaAvanzadaUsuarioForm(request.GET or None)
    usuarios = Usuario.objects.all()
    if formulario.is_valid():
        rol = formulario.cleaned_data.get('rol')
        direccion = formulario.cleaned_data.get('direccion')
        if rol:
            usuarios = usuarios.filter(rol__in=rol)
        if direccion:
            usuarios = usuarios.filter(direccion__icontains=direccion)
    return render(request, 'formularios/leer_usuarios.html', {
        'usuarios': usuarios,
        'formulario': formulario,
    })

@permission_required('tienda.change_usuario')
def editar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    formulario = UsuarioModelForm(request.POST or None, instance=usuario)
    if formulario.is_valid():
        formulario.save()
        return redirect("leer_usuarios")
    return render(request, 'formularios/editar_usuario.html', {"formulario": formulario, "usuario": usuario})

@permission_required('tienda.delete_usuario')
def eliminar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == "POST":
        usuario.delete()
        return redirect("lista_usuarios")
    return render(request, 'formularios/eliminar_usuario.html', {"usuario": usuario})

# CRUD para Órdenes
@permission_required('tienda.add_orden')
def crear_orden(request):
    formulario = OrdenModelForm(request.POST or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('lista_ordenes')
    return render(request, 'formularios/crear_orden.html', {'formulario': formulario})

@permission_required('tienda.view_orden')
def leer_ordenes(request):
    ordenes = Orden.objects.all()
    return render(request, 'formularios/leer_ordenes.html', {'ordenes': ordenes})

@permission_required('tienda.change_orden')
def editar_orden(request, pk):
    orden = get_object_or_404(Orden, pk=pk)
    formulario = OrdenModelForm(request.POST or None, instance=orden)
    if formulario.is_valid():
        formulario.save()
        return redirect('leer_ordenes')
    return render(request, 'formularios/editar_orden.html', {'formulario': formulario, 'orden': orden})

@permission_required('tienda.delete_orden')
def eliminar_orden(request, pk):
    orden = get_object_or_404(Orden, pk=pk)
    if request.method == 'POST':
        orden.delete()
        return redirect('leer_ordenes')
    return render(request, 'formularios/eliminar_orden.html', {'orden': orden})

@permission_required('tienda.add_provedor')
def crear_proveedor(request):
    formulario = ProvedorModelForm(request.POST or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('lista_proveedores')
    return render(request, 'formularios/crear_provedor.html', {'formulario': formulario})

@permission_required('tienda.view_provedor')
def leer_proveedores(request):
    proveedores = Provedor.objects.all()
    return render(request, 'formularios/leer_proveedores.html', {'provedores': proveedores})

@permission_required('tienda.change_provedor')
def editar_proveedor(request, pk):
    provedor = get_object_or_404(Provedor, pk=pk)
    formulario = ProvedorModelForm(request.POST or None, instance=provedor)
    if formulario.is_valid():
        formulario.save()
        return redirect('leer_proveedores')
    return render(request, 'formularios/editar_provedor.html', {'formulario': formulario, 'provedor': provedor})

@permission_required('tienda.delete_provedor')
def eliminar_proveedor(request, pk):
    provedor = get_object_or_404(Provedor, pk=pk)
    if request.method == 'POST':
        provedor.delete()
        return redirect('leer_proveedores')
    return render(request, 'formularios/eliminar_provedor.html', {'provedor': provedor})

# CRUD para Inventarios

@permission_required('tienda.add_inventario')
def crear_inventario(request):
    formulario = InventarioModelForm(request.POST or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('lista_inventarios')
    return render(request, 'formularios/crear_inventario.html', {'formulario': formulario})

@permission_required('tienda.view_inventario')
def leer_inventarios(request):
    inventarios = Inventario.objects.select_related('producto').all()
    return render(request, 'formularios/leer_inventarios.html', {'inventarios': inventarios})

@permission_required('tienda.change_inventario')
def editar_inventario(request, pk):
    inventario = get_object_or_404(Inventario, pk=pk)
    formulario = InventarioModelForm(request.POST or None, instance=inventario)
    if formulario.is_valid():
        formulario.save()
        return redirect('leer_inventarios')
    return render(request, 'formularios/editar_inventario.html', {'formulario': formulario, 'inventario': inventario})

@permission_required('tienda.delete_inventario')
def eliminar_inventario(request, pk):
    inventario = get_object_or_404(Inventario, pk=pk)
    if request.method == 'POST':
        inventario.delete()
        return redirect('leer_inventarios')
    return render(request, 'formularios/eliminar_inventario.html', {'inventario': inventario})

# CRUD para Tarjetas

@permission_required('tienda.add_tarjeta')
def crear_tarjeta(request):
    formulario = TarjetaModelForm(request.POST or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('lista_tarjetas')
    return render(request, 'formularios/crear_tarjeta.html', {'formulario': formulario})

@permission_required('tienda.view_tarjeta')
def leer_tarjetas(request):
    tarjetas = Tarjeta.objects.select_related('usuario').all()
    return render(request, 'formularios/leer_tarjetas.html', {'tarjetas': tarjetas})

@permission_required('tienda.change_tarjeta')
def editar_tarjeta(request, pk):
    tarjeta = get_object_or_404(Tarjeta, pk=pk)
    formulario = TarjetaModelForm(request.POST or None, instance=tarjeta)
    if formulario.is_valid():
        formulario.save()
        return redirect('leer_tarjetas')
    return render(request, 'formularios/editar_tarjeta.html', {'formulario': formulario, 'tarjeta': tarjeta})

@permission_required('tienda.delete_tarjeta')
def eliminar_tarjeta(request, pk):
    tarjeta = get_object_or_404(Tarjeta, pk=pk)
    if request.method == 'POST':
        tarjeta.delete()
        return redirect('leer_tarjetas')
    return render(request, 'formularios/eliminar_tarjeta.html', {'tarjeta': tarjeta})

# CRUD para Categorías

@permission_required('tienda.add_categoria')
def crear_categoria(request):
    formulario = CategoriaModelForm(request.POST or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('leer_categorias')
    return render(request, 'formularios/crear_categoria.html', {'formulario': formulario})

@permission_required('tienda.view_categoria')
def leer_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'formularios/leer_categorias.html', {'categorias': categorias})

@permission_required('tienda.change_categoria')
def editar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    formulario = CategoriaModelForm(request.POST or None, instance=categoria)
    if formulario.is_valid():
        formulario.save()
        return redirect('leer_categorias')
    return render(request, 'formularios/editar_categoria.html', {'formulario': formulario, 'categoria': categoria})

@permission_required('tienda.delete_categoria')
def eliminar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        return redirect('leer_categorias')
    return render(request, 'formularios/eliminar_categoria.html', {'categoria': categoria})

def asignar_grupo(usuario):
    """Asigna el grupo según el rol del usuario."""
    if usuario.rol == Usuario.CLIENTE:
        grupo = Group.objects.get(name='Clientes')
    elif usuario.rol == Usuario.GERENTE:
        grupo = Group.objects.get(name='Gerentes')
    else:
        return  # Si no hay un grupo para este rol, no hacer nada
    usuario.groups.add(grupo)

def registro_usuario(request):
    """Vista para registrar un nuevo usuario."""
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)  # Evita el guardado inmediato
            usuario.save()  # Guarda después de realizar validaciones
            asignar_permisos(usuario)  # Asigna los permisos adecuados
            return redirect('login')  # Redirigir al login tras el registro exitoso
    else:
        form = RegistroUsuarioForm()

    return render(request, 'registro/registro_usuario.html', {'formulario': form})

def asignar_permisos(usuario):
    """Asigna los permisos correspondientes según el rol del usuario."""
    permisos_cliente = ['view_producto', 'add_orden']  # Corrige los permisos
    permisos_gerente = ['view_orden', 'change_producto']

    if usuario.rol == Usuario.CLIENTE:
        for permiso in permisos_cliente:
            permiso_obj = Permission.objects.filter(codename=permiso).first()
            if permiso_obj:
                usuario.user_permissions.add(permiso_obj)

    elif usuario.rol == Usuario.GERENTE:
        for permiso in permisos_gerente:
            permiso_obj = Permission.objects.filter(codename=permiso).first()
            if permiso_obj:
                usuario.user_permissions.add(permiso_obj)
def logout_view(request):
    logout(request)
    request.session.flush()  # Elimina todas las variables de sesión
    return redirect('login')  # Redirigir a la página de login

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