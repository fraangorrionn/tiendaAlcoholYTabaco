from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Prefetch, Q
from .models import *
from .serializers import *
from rest_framework import viewsets
from django.contrib.auth.models import Group
from .forms import *
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny
from oauth2_provider.models import AccessToken 
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework import status

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

    ordenes = Orden.objects.prefetch_related(
        'usuario',
        'detalleorden_set__producto'
    ).order_by(ordering)

    serializer = OrdenSerializer(ordenes, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def lista_usuarios_api(request):
    """
    Devuelve la lista de todos los usuarios registrados.
    """
    usuarios = Usuario.objects.all()
    serializer = UsuarioSerializer(usuarios, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

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

#--------------------------------------Formularios POST------------------------------------------------
@api_view(['POST'])
def crear_producto_api(request): 
    # Crea un nuevo producto con validaciones personalizadas.

    productoCreateSerializer = ProductoCreateSerializer(data=request.data)

    if productoCreateSerializer.is_valid():
        try:
            productoCreateSerializer.save()
            return Response("Producto Creado", status=status.HTTP_201_CREATED)

        except serializers.ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            print(repr(error))
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        print("❌ Errores de validación:", productoCreateSerializer.errors)
        return Response(productoCreateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def crear_orden_api(request): 
    print(f"🔍 Datos recibidos en API-REST: {request.data}")  # 🔹 Agregar debug para ver qué datos llegan

    datos = request.data.copy()
    archivo = request.FILES.get('archivo_adjunto', None)

    if archivo:
        datos['archivo_adjunto'] = archivo

    ordenCreateSerializer = OrdenSerializerCreate(data=datos)

    if ordenCreateSerializer.is_valid():
        try:
            ordenCreateSerializer.save()
            return Response("Orden Creada", status=status.HTTP_201_CREATED)

        except serializers.ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            print(f"⚠️ Error inesperado en API-REST: {repr(error)}")
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    else:
        print(f"❌ Errores de validación en API-REST: {ordenCreateSerializer.errors}")
        return Response(ordenCreateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def crear_proveedor_api(request): 
    # Crea un nuevo proveedor con validaciones personalizadas.
    
    proveedorCreateSerializer = ProveedorSerializerCreate(data=request.data)

    if proveedorCreateSerializer.is_valid():
        try:
            proveedorCreateSerializer.save()
            return Response("Proveedor Creado", status=status.HTTP_201_CREATED)

        except serializers.ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            print(repr(error))
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        print("❌ Errores de validación:", proveedorCreateSerializer.errors)
        return Response(proveedorCreateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def crear_favoritos_api(request): 
    # Agrega un producto a los favoritos de un usuario.

    favoritosCreateSerializer = FavoritosSerializerCreate(data=request.data)
    print("📩 Datos recibidos en la petición:", request.data)

    if favoritosCreateSerializer.is_valid():
        try:
            favoritosCreateSerializer.save()
            return Response("Producto agregado a Favoritos", status=status.HTTP_201_CREATED)

        except serializers.ValidationError as error:
            print("❌ Error de validación en el guardado:", error.detail)
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            print("🔥 Error inesperado:", repr(error))
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        print("❌ Errores de validación:", favoritosCreateSerializer.errors)
        return Response(favoritosCreateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def crear_usuario_api(request):
    """
    Tengo que crear un usuario por la relacion con favoritos
    """
    usuarioSerializer = UsuarioCreateSerializer(data=request.data)

    if usuarioSerializer.is_valid():
        try:
            usuarioSerializer.save()
            return Response("Usuario Creado", status=status.HTTP_201_CREATED)

        except serializers.ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            print(repr(error))
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    print("❌ Errores de validación:", usuarioSerializer.errors)
    return Response(usuarioSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


#--------------------------------------Formularios PUT-------------------------------------------------
@api_view(['PUT'])
def editar_producto_api(request, producto_id):
    # Edtia completamente un producto existente.

    try:
        producto = Producto.objects.get(id=producto_id)
    except Producto.DoesNotExist:
        return Response({"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    productoSerializer = ProductoCreateSerializer(data=request.data, instance=producto)

    if productoSerializer.is_valid():
        try:
            productoSerializer.save()
            return Response("Producto EDITADO", status=status.HTTP_200_OK)

        except serializers.ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(productoSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PUT'])
def editar_orden_api(request, orden_id):
    # Edita completamente una orden existente, incluyendo el archivo adjunto.
    
    print(f"📌 Datos recibidos en la API (JSON): {request.data}") 

    try:
        orden = Orden.objects.get(id=orden_id)
    except Orden.DoesNotExist:
        return Response({"error": "Orden no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    datos = request.data.copy()  # Copia los datos del request
    archivo = request.FILES.get('archivo_adjunto', None)  # Obtener archivo si se envía uno

    # Agregar archivo a los datos si está presente
    if archivo:
        datos['archivo_adjunto'] = archivo

    ordenSerializer = OrdenSerializerCreate(data=datos, instance=orden, partial=True)  # `partial=True` permite actualizar campos opcionales

    if ordenSerializer.is_valid():
        try:
            ordenSerializer.save()
            return Response("Orden EDITADA", status=status.HTTP_200_OK)

        except serializers.ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    else:
        return Response(ordenSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
@api_view(['PUT'])
def editar_proovedor_api(request, proveedor_id):
    # Actualiza completamente un proveedor existente.
    
    print(f"📌 Datos recibidos en la API (JSON): {request.data}") 

    try:
        proveedor = Proveedor.objects.get(id=proveedor_id)
    except Proveedor.DoesNotExist:
        return Response({"error": "Proveedor no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    proveedorSerializer = ProveedorSerializerCreate(data=request.data, instance=proveedor)

    if proveedorSerializer.is_valid():
        try:
            proveedorSerializer.save()
            return Response("Proveedor EDITADO", status=status.HTTP_200_OK)

        except serializers.ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(proveedorSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def editar_favoritos_api(request, favorito_id):
    print(f"📌 Datos recibidos en la API (JSON): {request.data}") 

    try:
        favorito = Favoritos.objects.get(id=favorito_id)
    except Favoritos.DoesNotExist:
        print(f"❌ ERROR: Entrada en Favoritos con ID {favorito_id} no encontrada")
        return Response({"error": "Favorito no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    #Serializador con instancia existente (edición)
    favoritosSerializer = FavoritosSerializerCreate(instance=favorito, data=request.data)

    #Verificar si los datos pasan la validación
    if favoritosSerializer.is_valid():
        try:
            print(f"✅ Datos validados antes de guardar: {favoritosSerializer.validated_data}")  # Ver qué datos se guardarán
            favoritosSerializer.save()
            print("✔️ Favorito editado exitosamente en la base de datos.")
            return Response("Favorito EDITADO", status=status.HTTP_200_OK)

        except serializers.ValidationError as error:
            print(f"❌ ERROR en validación al guardar: {error.detail}")
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

        except Exception as error:
            print(f"🔥 ERROR inesperado al guardar: {repr(error)}")
            return Response({"error": repr(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    else:
        print(f"❌ ERROR en validación: {favoritosSerializer.errors}")
        return Response(favoritosSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
#--------------------------------------Formularios PATCH-------------------------------------------------

@api_view(['PATCH'])
def actualizar_nombre_producto_api(request, producto_id):
    # Permite actualizar solo el nombre de un producto.

    try:
        producto = Producto.objects.get(id=producto_id)
    except Producto.DoesNotExist:
        return Response({"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ProductoActualizarNombreSerializer(data=request.data, instance=producto)

    if serializer.is_valid():
        try:
            serializer.save()
            return Response("Producto Actualizado", status=status.HTTP_200_OK)
        except Exception as error:
            print(repr(error))  # Se imprime en consola para depuración
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])    
def actualizar_estado_orden_api(request, orden_id):
    # Permite actualizar solo el estado de una orden sin afectar el archivo adjunto.
    
    try:
        orden = Orden.objects.get(id=orden_id)
    except Orden.DoesNotExist:
        return Response({"error": "Orden no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    datos = request.data.copy()  # Copia los datos del request

    serializer = OrdenActualizarEstadoSerializer(instance=orden, data=datos, partial=True)  # `partial=True` permite actualizar solo los campos enviados

    if serializer.is_valid():
        try:
            serializer.save()
            return Response("Orden Actualizada", status=status.HTTP_200_OK)
        except Exception as error:
            print(f"❌ Error inesperado: {repr(error)}")
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        print(f"⚠️ Errores en validación: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
@api_view(['PATCH'])    
def actualizar_contacto_proveedor_api(request, proveedor_id):
    # Permite actualizar solo el contacto de un proveedor.
    
    try:
        proveedor = Proveedor.objects.get(id=proveedor_id)
    except Proveedor.DoesNotExist:
        return Response({"error": "Proveedor no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ProveedorActualizarContactoSerializer(data=request.data, instance=proveedor)

    if serializer.is_valid():
        try:
            serializer.save()
            return Response("Proveedor Actualizado", status=status.HTTP_200_OK)
        except Exception as error:
            print(repr(error))
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PATCH'])    
def actualizar_prioridad_favoritos_api(request, favorito_id):
    # Permite actualizar solo la prioridad o las notas de una entrada en Favoritos.
    
    try:
        favorito = Favoritos.objects.get(id=favorito_id)
    except Favoritos.DoesNotExist:
        return Response({"error": "Favorito no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    serializer = FavoritosSerializerActualizarPrioridad(data=request.data, instance=favorito)

    if serializer.is_valid():
        try:
            serializer.save()
            return Response("Favorito Actualizado", status=status.HTTP_200_OK)
        except Exception as error:
            print(repr(error))
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




#--------------------------------------Formularios DELETE-------------------------------------------------

@api_view(['DELETE'])
def eliminar_producto_api(request, producto_id):
    # Elimina un producto existente.
    
    try:
        producto = Producto.objects.get(id=producto_id)
    except Producto.DoesNotExist:
        return Response({"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    try:
        producto.delete()
        return Response("Producto ELIMINADO", status=status.HTTP_200_OK)
    except Exception as error:
        return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

import os
from django.conf import settings

@api_view(['DELETE'])
def eliminar_orden_api(request, orden_id):
    # Elimina una orden y su archivo adjunto si existe.
    
    try:
        orden = Orden.objects.get(id=orden_id)
    except Orden.DoesNotExist:
        return Response({"error": "Orden no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    try:
        # 📌 Verificar si la orden tiene un archivo adjunto y eliminarlo
        if orden.archivo_adjunto:
            archivo_path = os.path.join(settings.MEDIA_ROOT, str(orden.archivo_adjunto))
            if os.path.exists(archivo_path):
                os.remove(archivo_path)  # Eliminar archivo físicamente
        
        orden.delete()  # Eliminar la orden de la base de datos

        return Response("Orden y archivo adjunto eliminados correctamente.", status=status.HTTP_200_OK)
    
    except Exception as error:
        print(f"❌ Error inesperado: {repr(error)}")
        return Response({"error": repr(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
@api_view(['DELETE'])
def eliminar_proveedor_api(request, proveedor_id):
    try:
        proveedor = Proveedor.objects.get(id=proveedor_id)
    except Proveedor.DoesNotExist:
        return Response({"error": "Proveedor no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    try:
        proveedor.delete()
        return Response("Proveedor ELIMINADO", status=status.HTTP_200_OK)
    except Exception as error:
        return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def eliminar_favoritos_api(request, favorito_id):
    try:
        favorito = Favoritos.objects.get(id=favorito_id)
    except Favoritos.DoesNotExist:
        return Response({"error": "Favorito no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    try:
        favorito.delete()
        return Response("Favorito ELIMINADO", status=status.HTTP_200_OK)
    except Exception as error:
        return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ViewSets
class ProductoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para manejar todas las operaciones CRUD de Producto.
    """
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

    def create(self, request, *args, **kwargs):
        serializer = ProductoCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Producto Creado"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        producto = self.get_object()
        serializer = ProductoCreateSerializer(instance=producto, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Producto Editado"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        producto = self.get_object()
        serializer = ProductoActualizarNombreSerializer(instance=producto, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Producto Actualizado"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        producto = self.get_object()
        producto.delete()
        return Response({"message": "Producto Eliminado"}, status=status.HTTP_200_OK)
    
#--------------------------------------REGISTRO USUARIO-------------------------------------------------
# views.py
from rest_framework import generics
from rest_framework.permissions import AllowAny
    
class registrar_usuario(generics.CreateAPIView):
    serializer_class = UsuarioSerializerRegistro
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializers = UsuarioSerializerRegistro(data=request.data)

        if serializers.is_valid():
            try:
                rol = request.data.get('rol')

                user = Usuario.objects.create(
                    username = serializers.validated_data["username"], 
                    email=serializers.validated_data["email"], 
                    password = serializers.data.get("password1"),
                    rol= rol,
                    direccion=serializers.validated_data.get("direccion", "sin_direccion"),
                    telefono=serializers.validated_data.get("telefono", ""),
                )
                
                if(int(rol) == Usuario.CLIENTE):
                    grupo = Group.objects.get(name='Clientes')
                    grupo.user_set.add(user)
                    cliente = Cliente.objects.create( usuario = user)
                    cliente.save()

                elif(int(rol) == Usuario.GERENTE):
                    grupo = Group.objects.get(name='Gerentes') 
                    grupo.user_set.add(user)
                    gerente = Gerente.objects.create(usuario = user)
                    gerente.save()

                usuarioSerializado = UsuarioSerializer(user)
                
                return Response(usuarioSerializado.data)
            except Exception as error:
                print(repr(error))
                return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        


from oauth2_provider.models import AccessToken     
@api_view(['GET'])
def obtener_usuario_token(request,token):
    ModeloToken = AccessToken.objects.get(token=token)
    usuario = Usuario.objects.get(id=ModeloToken.user_id)
    serializer = UsuarioSerializer(usuario)
    return Response(serializer.data)

#--------------------------------------GET USUARIOS-------------------------------------------------

@api_view(['GET'])
def listar_ordenes_usuario(request):
    if not request.user.is_authenticated:
        return Response({"error": "No estás autenticado."}, status=status.HTTP_401_UNAUTHORIZED)

    print(f"Usuario autenticado: {request.user.username}")

    # Filtrar órdenes del usuario autenticado
    ordenes = Orden.objects.filter(usuario=request.user)
    print(f"Órdenes encontradas: {ordenes}")

    # Serializar los resultados
    pedido_serializer = OrdenSerializer(ordenes, many=True)

    return Response(pedido_serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def listar_favoritos_usuario(request):
    if not request.user.is_authenticated:
        return Response({"error": "No estás autenticado."}, status=status.HTTP_401_UNAUTHORIZED)

    print(f"Usuario autenticado: {request.user.username}")

    # Filtrar productos favoritos del usuario autenticado
    favoritos = Favoritos.objects.filter(usuario=request.user)
    print(f"Favoritos encontrados: {favoritos}")

    # Serializar los resultados
    favorito_serializer = FavoritoSerializer(favoritos, many=True)

    return Response(favorito_serializer.data, status=status.HTTP_200_OK)



#--------------------------------------POST USUARIOS-------------------------------------------------

@api_view(['POST'])
def crear_orden_usuario(request):
    
    if not request.user.is_authenticated:
        return Response({"error": "No estás autenticado."}, status=status.HTTP_401_UNAUTHORIZED)

    data = request.data.copy()
    data['usuario'] = request.user.id  # Asociamos la orden al usuario autenticado

    orden_serializer = OrdenSerializerCreate(data=data)

    if orden_serializer.is_valid():
        try:
            orden_serializer.save()
            return Response({"mensaje": "Orden creada con éxito"}, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({"error": repr(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(orden_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def crear_favorito_usuario(request):
    
    if not request.user.is_authenticated:
        return Response({"error": "No estás autenticado."}, status=status.HTTP_401_UNAUTHORIZED)

    data = request.data.copy()
    data['usuario'] = request.user.id  # Asociamos el favorito al usuario autenticado

    favorito_serializer = FavoritosSerializerCreate(data=data)

    if favorito_serializer.is_valid():
        try:
            favorito_serializer.save()
            return Response({"mensaje": "Producto agregado a favoritos"}, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({"error": repr(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(favorito_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
