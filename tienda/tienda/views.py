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

def lista_usuarios(request):
    if not request.user.is_authenticated or request.user.rol != Usuario.ADMINISTRADOR:
        return redirect('/accounts/login/')

    usuarios = Usuario.objects.all()
    return render(request, 'Paginas/usuarios_list.html', {'usuarios': usuarios})

def lista_productos(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')

    productos = Producto.objects.prefetch_related('categorias').order_by('-precio')
    return render(request, 'Paginas/productos_list.html', {'productos': productos})

def lista_ordenes(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')

    if request.user.rol == Usuario.CLIENTE:
        ordenes = Orden.objects.filter(usuario=request.user).select_related('usuario').order_by('-fecha_orden')[:10]
    elif request.user.rol in [Usuario.ADMINISTRADOR, Usuario.GERENTE]:
        ordenes = Orden.objects.select_related('usuario').order_by('-fecha_orden')[:10]
    else:
        return redirect('/accounts/login/')

    return render(request, 'Paginas/ordenes_list.html', {'ordenes': ordenes})

def lista_detalles_orden(request):
    if not request.user.is_authenticated or request.user.rol not in [Usuario.ADMINISTRADOR, Usuario.GERENTE]:
        return redirect('/accounts/login/')

    detalles = DetalleOrden.objects.select_related('producto', 'orden').all()

    for detalle in detalles:
        detalle.subtotal = detalle.cantidad * detalle.precio_unitario - detalle.descuento_aplicado

    return render(request, 'Paginas/detalles_orden_list.html', {'detalles': detalles})

def lista_proveedores(request):
    if not request.user.is_authenticated or request.user.rol != Usuario.GERENTE:
        return redirect('/accounts/login/')

    proveedores = Provedor.objects.prefetch_related('productos')
    return render(request, 'Paginas/proveedor_list.html', {'proveedores': proveedores})

def lista_inventarios(request):
    if not request.user.is_authenticated or request.user.rol != Usuario.GERENTE:
        return redirect('/accounts/login/')

    inventarios = Inventario.objects.select_related('producto').filter(cantidad_disponible__lt=F('minimo_requerido')).order_by('cantidad_disponible')
    return render(request, 'Paginas/inventarios_list.html', {'inventarios': inventarios})

def lista_tarjetas(request):
    if not request.user.is_authenticated or request.user.rol != Usuario.ADMINISTRADOR:
        return redirect('/accounts/login/')

    tarjetas = Tarjeta.objects.select_related('usuario').all()
    context = {
        'tarjetas': tarjetas,
        'today': timezone.now().date()
    }
    return render(request, 'Paginas/tarjetas_list.html', context)

def lista_favoritos(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')

    favoritos = Favoritos.objects.select_related('usuario', 'producto').filter(prioridad__gte=2)
    return render(request, 'Paginas/favoritos_list.html', {'favoritos': favoritos})

def lista_reclamos(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')

    mostrar_pendientes = request.GET.get('pendientes', 'false') == 'true'

    if mostrar_pendientes:
        reclamos = Reclamo.objects.select_related('usuario', 'detalle_orden').filter(respuesta__isnull=True)
    else:
        reclamos = Reclamo.objects.select_related('usuario', 'detalle_orden')

    return render(request, 'Paginas/reclamos_list.html', {'reclamos': reclamos, 'mostrar_pendientes': mostrar_pendientes})

def lista_categorias(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')

    categorias = Categoria.objects.filter(estado='activo').order_by('-prioridad')
    return render(request, 'Paginas/categorias_list.html', {'categorias': categorias})

def lista_producto_categoria(request):
    if not request.user.is_authenticated or request.user.rol not in [Usuario.ADMINISTRADOR, Usuario.GERENTE]:
        return redirect('/accounts/login/')

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

def ordenes_recientes(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')

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
def crear_usuario(request):
    formulario = UsuarioModelForm(request.POST or None)
    if request.method == "POST":
        if formulario.is_valid():
            formulario.save()
            return redirect("lista_usuarios")  # Redirige a la lista de usuarios
    return render(request, 'formularios/crear_usuario.html', {"formulario": formulario})

# Leer la lista de usuarios
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


# Actualizar un usuario existente
def editar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)

    if request.method == "POST":
        formulario = UsuarioModelForm(request.POST, instance=usuario)
        if formulario.is_valid():
            formulario.save()
            return redirect("leer_usuarios")
    else:
        formulario = UsuarioModelForm(instance=usuario)

    return render(request, 'formularios/editar_usuario.html', {"formulario": formulario, "usuario": usuario})



# Eliminar un usuario
def eliminar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)  # Obtén el usuario o lanza un 404

    if request.method == "POST":
        usuario.delete()
        print(f"Usuario {usuario.nombre} eliminado correctamente.")  # Depuración
        return redirect("leer_usuarios")  # Asegúrate de que esta URL esté definida
    return render(request, 'formularios/eliminar_usuario.html', {"usuario": usuario})



def crear_orden(request):
    if request.method == "POST":
        formulario = OrdenModelForm(request.POST, request.FILES, request=request)  # Pasamos el request al formulario
        if formulario.is_valid():
            formulario.save()  # Guardar la orden con el usuario logueado asignado automáticamente
            return redirect('lista_ordenes')  # Redirige a la lista de órdenes
    else:
        formulario = OrdenModelForm(request=request)  # Pasamos el request también en el GET
    return render(request, 'formularios/crear_orden.html', {'formulario': formulario})

def leer_ordenes(request):
    formulario = BusquedaAvanzadaOrdenForm(request.GET or None)
    ordenes = Orden.objects.select_related('usuario').all()

    if formulario.is_valid():
        estado = formulario.cleaned_data.get('estado')
        usuario = formulario.cleaned_data.get('usuario')
        total_min = formulario.cleaned_data.get('total_min')
        total_max = formulario.cleaned_data.get('total_max')

        # Aplicar filtros si los datos están presentes
        if estado:
            ordenes = ordenes.filter(estado=estado)
        if usuario:
            ordenes = ordenes.filter(usuario=usuario)
        if total_min is not None:
            ordenes = ordenes.filter(total__gte=total_min)
        if total_max is not None:
            ordenes = ordenes.filter(total__lte=total_max)

    return render(request, 'formularios/leer_ordenes.html', {
        "ordenes": ordenes,
        "formulario": formulario,  # Pasamos el formulario al template
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
    # Instanciar el formulario con los datos GET
    formulario = BusquedaAvanzadaProvedorForm(request.GET or None)
    provedores = Provedor.objects.all()

    if formulario.is_valid():
        # Obtener datos limpios del formulario
        nombre = formulario.cleaned_data.get('nombre')
        contacto = formulario.cleaned_data.get('contacto')
        telefono = formulario.cleaned_data.get('telefono')

        # Aplicar filtros
        if nombre:
            provedores = provedores.filter(nombre__icontains=nombre)
        if contacto:
            provedores = provedores.filter(contacto__icontains=contacto)
        if telefono:
            provedores = provedores.filter(telefono__icontains=telefono)

    return render(request, 'formularios/leer_proveedores.html', {
        "provedores": provedores,
        "formulario": formulario,
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
    formulario = BusquedaAvanzadaInventarioForm(request.GET or None)
    inventarios = Inventario.objects.select_related('producto').all()

    if formulario.is_valid():
        # Obtener datos limpios del formulario
        producto = formulario.cleaned_data.get('producto')
        ubicacion = formulario.cleaned_data.get('ubicacion')
        cantidad_min = formulario.cleaned_data.get('cantidad_min')
        cantidad_max = formulario.cleaned_data.get('cantidad_max')

        # Aplicar filtros
        if producto:
            inventarios = inventarios.filter(producto__nombre__icontains=producto)
        if ubicacion:
            inventarios = inventarios.filter(ubicacion__icontains=ubicacion)
        if cantidad_min is not None:
            inventarios = inventarios.filter(cantidad_disponible__gte=cantidad_min)
        if cantidad_max is not None:
            inventarios = inventarios.filter(cantidad_disponible__lte=cantidad_max)

    return render(request, 'formularios/leer_inventarios.html', {
        "inventarios": inventarios,
        "formulario": formulario,  # Pasar el formulario al template
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
    formulario = BusquedaAvanzadaTarjetaForm(request.GET or None)
    tarjetas = Tarjeta.objects.select_related('usuario').all()

    if formulario.is_valid():
        # Obtener datos limpios del formulario
        usuario = formulario.cleaned_data.get('usuario')
        tipo = formulario.cleaned_data.get('tipo')
        fecha_inicio = formulario.cleaned_data.get('fecha_inicio')
        fecha_fin = formulario.cleaned_data.get('fecha_fin')

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
        "formulario": formulario,
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
    formulario = BusquedaAvanzadaCategoriaForm(request.GET or None)
    categorias = Categoria.objects.all()

    if formulario.is_valid():
        # Obtener datos limpios del formulario
        nombre = formulario.cleaned_data.get('nombre')
        estado = formulario.cleaned_data.get('estado')
        prioridad_min = formulario.cleaned_data.get('prioridad_min')
        prioridad_max = formulario.cleaned_data.get('prioridad_max')

        # Aplicar filtros
        if nombre:
            categorias = categorias.filter(nombre__icontains=nombre)
        if estado:
            categorias = categorias.filter(estado=estado)
        if prioridad_min is not None:
            categorias = categorias.filter(prioridad__gte=prioridad_min)
        if prioridad_max is not None:
            categorias = categorias.filter(prioridad__lte=prioridad_max)

    return render(request, 'formularios/leer_categorias.html', {
        'categorias': categorias,
        'formulario': formulario,  # Pasar el formulario al template
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

# Citas----------------------
def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)  # Iniciar sesión automáticamente tras registrarse
            return redirect('index')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'registro/registro_usuario.html', {'form': form})

def seleccionar_producto(request):
    if request.method == 'POST':
        form = ProductoProveedorForm(request.POST, request=request)
        if form.is_valid():
            producto = form.cleaned_data['producto']
            # Lógica adicional con el producto seleccionado
            return redirect('index')
    else:
        form = ProductoProveedorForm(request=request)
    return render(request, 'registro/seleccionar_producto.html', {'form': form})

def buscar_ordenes(request):
    ordenes = Orden.objects.all()

    # Filtrar por usuario logueado
    if request.user.rol == Usuario.CLIENTE:
        ordenes = ordenes.filter(usuario=request.user)

    if request.method == 'GET':
        form = BusquedaAvanzadaOrdenForm(request.GET, request=request)
        if form.is_valid():
            estado = form.cleaned_data.get('estado')
            total_min = form.cleaned_data.get('total_min')
            total_max = form.cleaned_data.get('total_max')

            # Aplicar filtros adicionales
            if estado:
                ordenes = ordenes.filter(estado=estado)
            if total_min is not None:
                ordenes = ordenes.filter(total__gte=total_min)
            if total_max is not None:
                ordenes = ordenes.filter(total__lte=total_max)
    else:
        form = BusquedaAvanzadaOrdenForm(request=request)

    return render(request, 'formularios/buscar_ordenes.html', {'form': form, 'ordenes': ordenes})

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