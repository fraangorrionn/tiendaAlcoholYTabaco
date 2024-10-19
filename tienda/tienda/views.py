from django.shortcuts import render
from .models import (
    Usuario, Producto, Orden, DetalleOrden, Provedor, 
    Inventario, Tarjeta, Favoritos, Reclamo, Categoria, 
    ProductoCategoria
)

def index(request):
    return render(request, 'index.html')

# Vista para listar Usuarios
def lista_usuario(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuario_list.html', {'usuarios': usuarios})

# Vista para listar Productos
def lista_producto(request):
    productos = Producto.objects.all()
    return render(request, 'producto_list.html', {'productos': productos})

# Vista para listar Órdenes
def lista_orden(request):
    ordenes = Orden.objects.all()
    return render(request, 'orden_list.html', {'ordenes': ordenes})

# Vista para listar Detalles de Orden
def lista_detalle_orden(request):
    detalles = DetalleOrden.objects.all()
    return render(request, 'detalle_orden_list.html', {'detalles': detalles})

# Vista para listar Proveedores
def lista_provedor(request):
    provedores = Provedor.objects.all()
    return render(request, 'provedor_list.html', {'provedores': provedores})

# Vista para listar Inventarios
def lista_inventario(request):
    inventarios = Inventario.objects.all()
    return render(request, 'inventario_list.html', {'inventarios': inventarios})

# Vista para listar Tarjetas
def lista_tarjeta(request):
    tarjetas = Tarjeta.objects.all()
    return render(request, 'tarjeta_list.html', {'tarjetas': tarjetas})

# Vista para listar Favoritos
def lista_favoritos(request):
    favoritos = Favoritos.objects.all()
    return render(request, 'favoritos_list.html', {'favoritos': favoritos})

# Vista para listar Reclamos
def lista_reclamo(request):
    reclamos = Reclamo.objects.all()
    return render(request, 'reclamo_list.html', {'reclamos': reclamos})

# Vista para listar Categorías
def lista_categoria(request):
    categorias = Categoria.objects.all()
    return render(request, 'categoria_list.html', {'categorias': categorias})

# Vista para listar Productos por Categoría
def lista_producto_categoria(request):
    productos_categoria = ProductoCategoria.objects.all()
    return render(request, 'producto_categoria_list.html', {'productos_categoria': productos_categoria})
