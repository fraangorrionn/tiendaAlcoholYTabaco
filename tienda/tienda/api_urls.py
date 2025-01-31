from django.urls import path

from  .api_views import *

urlpatterns = [
    path('api/', lista_productos_api, name='lista_productos_api'),
    path('api/detallados/', lista_productos_detallada_api, name='lista_productos_detallada_api'),
]