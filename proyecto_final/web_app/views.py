from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
from crud import repositories
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import numpy as np

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
    if len(mensajes) < 1:
        repositories.MensajeRepository().seed_metacritic_mensajes_data(data=data)
        mensajes = repositories.MensajeRepository().search(data=data)
        
    template = loader.get_template('mensajes_juego.html')
    context = {
        'mensajes' : mensajes,
        'num_mensajes': len(mensajes),
    }
    
    return HttpResponse(template.render(context, request))

def mensajes_por_usuario(request):
    data = repositories.MensajeRepository().quantity_per_user()
    
    template = loader.get_template('mensajes_usuarios.html')
    context = {
        'lista': data
    }
    
    return HttpResponse(template.render(context, request))

@csrf_exempt
def apariciones_formulario(request):
    if request.method == 'POST':
        data = request.POST
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        text = data.get('text')
        
        data = repositories.MensajeRepository().users_with_text_in_messages(start_date=start_date, end_date=end_date, text_search=text)
    
        context = {
            'list': data,
            'start_date': start_date,
            'end_date': end_date,
            'text': text
        }
        
        template = loader.get_template('apariciones_texto.html')
        return HttpResponse(template.render(context, request))
    else:
    
        template = loader.get_template('apariciones_form.html')
        
        return HttpResponse(template.render({}, request))

@csrf_exempt 
def media_mensajes_red_social(request):
    if request.method == 'POST':
        data = request.POST
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        
        data = repositories.MensajeRepository().average_messages_social_media(start_date=start_date, end_date=end_date)
        
        fig, ax = plt.subplots(figsize=(8, 6))

        x_labels = [d[0] for d in data]
        x_pos = np.linspace(0, len(x_labels)-1, len(x_labels))
        y_values = [d[1] for d in data]
        ax.bar(x_pos, y_values, color='blue')

        ax.set_xlabel('Red social')
        ax.set_ylabel('Cantidad de mensajes')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(x_labels, rotation=45, ha='right')

        plt.tight_layout()

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        
        context = {
            'list': data,
            'start_date': start_date,
            'end_date': end_date,
            'image': image_base64
        }
        
        template = loader.get_template('media_mensajes_result.html')
        return HttpResponse(template.render(context, request))
    else:
        template = loader.get_template('media_mensajes_form.html')
        return HttpResponse(template.render({}, request))
