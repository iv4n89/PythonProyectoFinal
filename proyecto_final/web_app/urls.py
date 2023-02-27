from . import views
from django.urls import path

urlpatterns = [
    path('lista-juegos', views.lista_juegos, name='test'),
    path('mensajes/<int:id_juego>', views.mensajes_juego, name='mensajes_juego'),
]
