from . import views
from django.urls import path

urlpatterns = [
    path('lista-juegos', views.lista_juegos, name='test'),
    path('mensajes/<int:id_juego>', views.mensajes_juego, name='mensajes_juego'),
    path('mensajes-por-usuario', views.mensajes_por_usuario, name='mensajes_por_usuario'),
    path('mensajes-apariciones', views.apariciones_formulario, name='apariciones_formulario'),
    path('mensajes-media', views.media_mensajes_red_social, name='media_social_media'),
]
