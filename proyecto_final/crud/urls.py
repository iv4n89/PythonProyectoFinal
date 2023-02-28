from django.urls import path, re_path
from . import views

urlpatterns = [
    path('plataforma/', views.PlataformaViewSet.as_view({'get': 'list'})),
    path('plataforma/create', views.PlataformaViewSet.as_view({'post': 'create'})),
    path('plataforma/search', views.PlataformaViewSet.as_view({ 'post': 'search' })),
    re_path(r'^plataforma/(?P<pk>[0-9]+)/$', views.PlataformaViewSet.as_view({
        'get': 'retrieve',
        'put': 'partial_update',
        'delete': 'destroy',
    })),
    path('juego/', views.JuegoViewSet.as_view({'get': 'list'})),
    path('juego/create', views.JuegoViewSet.as_view({'post': 'create'})),
    path('juego/seed', views.JuegoViewSet.as_view({ 'options': 'seed_data_base' })),
    path('juego/search', views.JuegoViewSet.as_view({ 'post': 'search' })),
    re_path(r'^juego/(?P<pk>[0-9]+)/$', views.JuegoViewSet.as_view({
        'get': 'retrieve',
        'put': 'partial_update',
        'delete': 'destroy',
    })),
    path('red-social/', views.RedSocialViewSet.as_view({'get': 'list'})),
    path('red-social/create', views.RedSocialViewSet.as_view({'post': 'create'})),
    path('red-social/search', views.RedSocialViewSet.as_view({ 'post': 'search' })),
    re_path(r'^red-social/(?P<pk>[0-9]+)/$', views.RedSocialViewSet.as_view({
        'get': 'retrieve',
        'put': 'partial_update',
        'delete': 'destroy'
    })),
    path('usuario/', views.UsuarioViewSet.as_view({'get': 'list'})),
    path('usuario/create', views.UsuarioViewSet.as_view({'post': 'create'})),
    path('usuario/search', views.UsuarioViewSet.as_view({ 'post': 'search' })),
    re_path(r'^usuario/(?P<pk>[0-9]+)/$', views.UsuarioViewSet.as_view({
        'get': 'retrieve',
        'put': 'partial_update',
        'delete': 'destroy'
    })),
    path('mensaje/', views.MensajeViewSet.as_view({'get': 'list'})),
    path('mensaje/per-user', views.MensajeViewSet.as_view({ 'get': 'quantity_per_user' })),
    path('mensaje/seed/metacritic', views.MensajeViewSet.as_view({ 'post': 'seed_metacritic_mensajes_data' })),
    path('mensaje/seed/playstoregames', views.MensajeViewSet.as_view({ 'options': 'seed_play_store_game_data' })),
    path('mensaje/search', views.MensajeViewSet.as_view({ 'post': 'search' })),
    path('mensaje/create', views.MensajeViewSet.as_view({'post': 'create'})),
    re_path(r'^mensaje/(?P<pk>[0-9]+)/$', views.MensajeViewSet.as_view({
        'get': 'retrieve',
        'put': 'partial_update',
        'delete': 'destroy'
    })),
]
