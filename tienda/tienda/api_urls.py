from django.urls import path

from  .api_views import *

urlpatterns = [
    path('ordenes',lista_ordenes),
    path('productos',lista_productos),
    path('usuarios',lista_usuarios),
]