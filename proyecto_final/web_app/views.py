from django.shortcuts import render, HttpResponse
from django.template import loader
from crud import repositories

# Create your views here.

card_borders = [
    'border-primary',
    'border-secondary',
    'border-success',
    'border-danger',
    'border-warning',
    'border-info',
    'border-dark',
]

card_bg = [
    'bg-primary',
    'bg-secondary',
    'bg-success',
    'bg-danger',
    'bg-warning',
    'bg-info',
    'bg-light',
    'bg-dark',
]

def lista_juegos(request):
    juegos = repositories.JuegoRepository().list()
    template = loader.get_template('lista_juegos.html')
    context = {
        'juegos': juegos,
        'borders': card_borders,
        'bg': card_bg,
    }
    return HttpResponse(template.render(context, request))

def mensajes_juego(request, id_juego):
    data = {
        "id_juego": id_juego
    }
    mensajes = repositories.MensajeRepository().search(data=data)
    template = loader.get_template('mensajes_juego.html')
    context = {
        'mensajes' : mensajes,
    }
    
    return HttpResponse(template.render(context, request))
