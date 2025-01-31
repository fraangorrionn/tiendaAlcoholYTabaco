from django.shortcuts import render
from .models import Producto, ProductoCategoria, Inventario

def lista_productos_api(request):
    productos = Producto.objects.all().values('id', 'nombre', 'precio', 'tipo', 'stock')
    return render(request, 'api/lista_productos_api.html', {'productos': productos})


def lista_productos_detallada_api(request):
    productos = Producto.objects.all()
    
    productos_detallados = []
    for producto in productos:
        categorias = ProductoCategoria.objects.filter(producto=producto).select_related('categoria')
        inventario = Inventario.objects.filter(producto=producto).first()
        
        productos_detallados.append({
            'id': producto.id,
            'nombre': producto.nombre,
            'precio': producto.precio,
            'tipo': producto.tipo,
            'stock': producto.stock,
            'categorias': [c.categoria.nombre for c in categorias],
            'cantidad_disponible': inventario.cantidad_disponible if inventario else 0
        })

    return render(request, 'api/lista_productos_detallada_api.html', {'productos': productos_detallados})


