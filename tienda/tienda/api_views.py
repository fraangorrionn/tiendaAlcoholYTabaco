from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework import status
from .forms import *
from django.db.models import Q,Prefetch
from django.contrib.auth.models import Group
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
def lista_ordenes(request):
    if request.user.rol == Usuario.CLIENTE:
        ordenes = Orden.objects.filter(usuario=request.user).select_related('usuario').order_by('-fecha_orden')[:10]
    else:
        ordenes = Orden.objects.select_related('usuario').order_by('-fecha_orden')[:10]
    #serializer = LibroSerializer(libros, many=True)
    serializer = OrdenSerializer(ordenes, many=True)
    return Response(serializer.data)