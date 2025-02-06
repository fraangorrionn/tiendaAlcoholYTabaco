from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Prefetch, Q
from .models import Producto, ProductoCategoria, Inventario, Orden, Proveedor, Inventario, Reclamo
from .serializers import ProductoDetalleSerializer, ProductoSerializer, OrdenSerializer, ProveedorSerializer, ReclamoSerializer

@api_view(['GET'])
def lista_productos_api(request):
    productos = Producto.objects.all()
    serializer = ProductoSerializer(productos, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def lista_productos_detallada_api(request):
    """
    Vista mejorada del listado de productos con filtros y búsqueda.
    """
    search = request.GET.get('search', '')
    ordering = request.GET.get('ordering', 'precio')  # Ordena por precio por defecto

    productos = Producto.objects.filter(
        nombre__icontains=search
    ).prefetch_related(
        Prefetch('productocategoria_set', queryset=ProductoCategoria.objects.select_related('categoria')),
        Prefetch('inventario')
    ).order_by(ordering)

    serializer = ProductoDetalleSerializer(productos, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def lista_ordenes_api(request):
    """
    Vista mejorada del listado de órdenes con información de usuario y productos.
    """
    search = request.GET.get('search', '')
    ordering = request.GET.get('ordering', '-fecha_orden')  # Ordena por fecha descendente

    ordenes = Orden.objects.filter(usuario__username__icontains=search).prefetch_related(
        'usuario',  # Relación con el usuario
        'detalleorden_set__producto'  # Relación con productos en la orden
    ).order_by(ordering)

    serializer = OrdenSerializer(ordenes, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def lista_proveedores_api(request):
    """
    Vista mejorada del listado de proveedores con productos que suministran.
    """
    proveedores = Proveedor.objects.prefetch_related('productos').all()

    serializer = ProveedorSerializer(proveedores, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Solo usuarios autenticados pueden acceder
def reclamo_list_view(request):
    reclamos = Reclamo.objects.all().select_related('usuario', 'detalle_orden')  # Optimización con select_related
    serializer = ReclamoSerializer(reclamos, many=True)
    return Response(serializer.data)

#----------------------------------------------Formularios---------------------------------------------------------------

# ---------------------- Búsqueda Simple de Producto ---------------------- #
@api_view(['GET'])
def busqueda_simple_producto(request):
    search = request.GET.get('search', '')

    if not search.strip():
        return Response({'error': 'Debe ingresar un término de búsqueda.'}, status=status.HTTP_400_BAD_REQUEST)

    productos = Producto.objects.filter(nombre__icontains=search)
    serializer = ProductoSerializer(productos, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# ---------------------- Búsqueda Avanzada de Producto ---------------------- #
@api_view(['GET'])
def busqueda_avanzada_producto(request):
    nombre = request.GET.get('nombre', '').strip()
    tipo = request.GET.get('tipo', '').strip()
    precio_min = request.GET.get('precio_min', None)
    precio_max = request.GET.get('precio_max', None)

    if not any([nombre, tipo, precio_min, precio_max]):
        return Response({'error': 'Debe especificar al menos un criterio de búsqueda.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        productos = Producto.objects.all()

        if nombre:
            productos = productos.filter(nombre__icontains=nombre)
        if tipo:
            productos = productos.filter(tipo=tipo)
        if precio_min:
            productos = productos.filter(precio__gte=float(precio_min))
        if precio_max:
            productos = productos.filter(precio__lte=float(precio_max))

        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except ValueError:
        return Response({'error': 'Los valores de precio deben ser números válidos.'}, status=status.HTTP_400_BAD_REQUEST)


# ---------------------- Búsqueda Avanzada de Órdenes ---------------------- #
@api_view(['GET'])
def busqueda_avanzada_orden(request):
    usuario = request.GET.get('usuario', '').strip()
    estado = request.GET.get('estado', '').strip()
    total_min = request.GET.get('total_min', None)
    total_max = request.GET.get('total_max', None)

    if not any([usuario, estado, total_min, total_max]):
        return Response({'error': 'Debe especificar al menos un criterio de búsqueda.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        ordenes = Orden.objects.all()

        if usuario:
            ordenes = ordenes.filter(usuario__username__icontains=usuario)
        if estado:
            ordenes = ordenes.filter(estado=estado)
        if total_min:
            ordenes = ordenes.filter(total__gte=float(total_min))
        if total_max:
            ordenes = ordenes.filter(total__lte=float(total_max))

        serializer = OrdenSerializer(ordenes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except ValueError:
        return Response({'error': 'Los valores de total deben ser números válidos.'}, status=status.HTTP_400_BAD_REQUEST)


# ---------------------- Búsqueda Avanzada de Proveedores ---------------------- #
@api_view(['GET'])
def busqueda_avanzada_proveedor(request):
    nombre = request.GET.get('nombre', '').strip()
    contacto = request.GET.get('contacto', '').strip()
    telefono = request.GET.get('telefono', '').strip()

    if not any([nombre, contacto, telefono]):
        return Response({'error': 'Debe especificar al menos un criterio de búsqueda.'}, status=status.HTTP_400_BAD_REQUEST)

    proveedores = Proveedor.objects.all()

    if nombre:
        proveedores = proveedores.filter(nombre__icontains=nombre)
    if contacto:
        proveedores = proveedores.filter(contacto__icontains=contacto)
    if telefono:
        proveedores = proveedores.filter(telefono__icontains=telefono)

    serializer = ProveedorSerializer(proveedores, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
