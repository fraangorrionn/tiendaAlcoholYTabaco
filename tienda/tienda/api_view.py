from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.db.models import Prefetch
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
