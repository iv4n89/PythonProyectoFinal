from django.urls import path, re_path
from . import views

urlpatterns = [
    path('juegos/', views.JuegoViewSet.as_view({'get': 'list'})),
    path('juegos/create', views.JuegoViewSet.as_view({'post': 'create'})),
    path('juegos/seed', views.JuegoViewSet.as_view({ 'options': 'seed_data_base' })),
    re_path(r'^juegos/(?P<pk>[0-9]+)/$', views.JuegoViewSet.as_view({
        'get': 'retrieve',
        'put': 'partial_update',
        'delete': 'destroy',
    })),
    path('red-social/', views.RedSocialViewSet.as_view({'get': 'list'})),
    path('red-social/create', views.RedSocialViewSet.as_view({'post': 'create'})),
    re_path(r'^red-social/(?P<pk>[0-9]+)/$', views.RedSocialViewSet.as_view({
        'get': 'retrieve',
        'put': 'partial_update',
        'delete': 'destroy'
    })),
    path('usuario/', views.UsuarioViewSet.as_view({'get': 'list'})),
    path('usuario/create', views.UsuarioViewSet.as_view({'post': 'create'})),
    re_path(r'^usuario/(?P<pk>[0-9]+)/$', views.UsuarioViewSet.as_view({
        'get': 'retrieve',
        'put': 'partial_update',
        'delete': 'destroy'
    })),
    path('mensaje/', views.MensajeViewSet.as_view({'get': 'list'})),
    path('mensaje/seed/metacritic', views.MensajeViewSet.as_view({ 'options': 'seed_metacritic_mensajes_data' })),
    path('mensaje/create', views.MensajeViewSet.as_view({'post': 'create'})),
    re_path(r'^mensaje/(?P<pk>[0-9]+)/$', views.MensajeViewSet.as_view({
        'get': 'retrieve',
        'put': 'partial_update',
        'delete': 'destroy'
    })),
]
