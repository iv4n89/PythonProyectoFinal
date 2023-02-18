from rest_framework import viewsets
from rest_framework.response import Response
import itertools
import csv
import json
from . import models
from . import serializers
from . import forms
import os
from django.conf import settings
from django.db.models import Q
from django.utils import timezone
import random

STATUS = {
    'OK': 200,
    'CREATED': 201,
    'NO_CONTENT': 204,
    'BAD_REQUEST': 400,
    'NOT_FOUND': 404,
}

class BaseViewSet(viewsets.ViewSet):
    serializer_class = None
    model_class = None

    def list(self, request):
        queryset = self.model_class.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=STATUS['CREATED'])
        return Response(serializer.errors, status=STATUS['BAD_REQUEST'])

    def retrieve(self, request, pk=None):
        queryset = self.model_class.objects.get(pk=pk)
        serializer = self.serializer_class(queryset)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        queryset = self.model_class.objects.get(pk=pk)
        serializer = self.serializer_class(
            queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=STATUS['BAD_REQUEST'])

    def destroy(self, request, pk=None):
        queryset = self.model_class.objects.get(pk=pk)
        queryset.delete()
        return Response(status=STATUS['NO_CONTENT'])

class PlataformaViewSet(BaseViewSet):
    model_class = models.Plataforma
    serializer_class = serializers.PlataformaSerializer

class JuegoViewSet(BaseViewSet):
    model_class = models.Juego
    serializer_class = serializers.JuegoSerializer
    
    def create(self, request):
        data = request.data
        if not isinstance(data['id_plataforma'], int):
            if isinstance(data['id_plataforma'], str):
                plataforma, created = models.Plataforma.objects.get_or_create(nombre=data['id_plataforma'])
                data['id_plataforma'] = plataforma.id
            if isinstance(data['id_plataforma'], dict):
                plataforma, crated = models.Plataforma.objects.get_or_create(nombre=data['id_plataforma']['nombre'])
                data['id_plataforma'] = plataforma.id
                
        serializer = self.serializer_class(data=data)
        
        if serializer.is_valid():
            return Response(serializer.data)
        
        return Response(serializer.error_messages, status=STATUS['BAD_REQUEST'])
    
    def partial_update(self, request, pk=None):
        queryset = self.model_class.objects.get(pk=pk)
        data = request.data
        
        if 'id_plataforma' in data and not isinstance(data['id_plataforma'], int):
            if isinstance(data['id_plataforma'], str):
                plataforma, created = models.Plataforma.objects.get_or_create(nombre=data['id_plataforma'])
                data['id_plataforma'] = plataforma.id
            if isinstance(data['id_plataforma'], dict):
                plataforma, crated = models.Plataforma.objects.get_or_create(nombre=data['id_plataforma']['nombre'])
                data['id_plataforma'] = plataforma.id
                
        serializer = self.serializer_class(
            queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=STATUS['BAD_REQUEST'])
        

    def seed_data_base(self, request):
        self.model_class.objects.all().delete()

        with open(os.path.join(settings.BASE_DIR, 'datos', 'metacritic_game_info.csv'), 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            juegos = []
            for row in reader:
                    
                if row['Title'] == 'Bad request' or row['Platform'] == 'not specified':
                    continue
                
                plataforma, created = models.Plataforma.objects.get_or_create(nombre=row['Platform'])
                
                juego = models.Juego(
                    titulo=row['Title'], 
                    id_plataforma=plataforma,
                    f_publicacion=row['Year']
                    )
                juegos.append(juego)

        self.model_class.objects.bulk_create(juegos)

        return Response('Los juegos se cargaron correctamente desde el csv')


class RedSocialViewSet(BaseViewSet):
    model_class = models.Red_social
    serializer_class = serializers.RedSocialSerializer


class UsuarioViewSet(BaseViewSet):
    model_class = models.Usuario
    serializer_class = serializers.UsuarioSerializer


class MensajeViewSet(BaseViewSet):
    model_class = models.Mensaje
    serializer_class = serializers.MensajeSerializer
    
    def create(self, request):
        data = request.data
        
        #red social
        if not isinstance(data['id_red_social'], int):
            if isinstance(data['id_red_social'], str):
                red_social, created = models.Red_social.objects.get_or_create(nombre=data['id_red_social'])
                data['id_red_social'] = red_social.id
            if isinstance(data['id_red_social'], dict):
                red_social, created = models.Red_social.objects.get_or_create(nombre=data['id_red_social']['nombre'], url=data['id_red_social']['url'])
                data['id_red_social'] = red_social.id
                
        #usuario
        if not isinstance(data['id_usuario'], int):
            if isinstance(data['id_usuario'], str):
                usuario = models.Usuario.objects.get(nick=data['id_usuario'])
                if usuario == None:
                    raise Exception('No se encuentra el usuario')
                data['id_usuario'] = usuario.id
            if isinstance(data['id_usuario'], dict):
                usuario = models.Usuario.objects.get(nick=data['id_usuario']['nick'])
                if usuario == None:
                    raise Exception('No se encuentra el usuario')
                data['id_usuario'] = usuario.id
                
        #juego
        if not isinstance(data['id_juego'], int):
            if isinstance(data['id_juego'], str):
                juego = models.Juego.objects.get(titulo=data['id_juego'])
                if juego == None:
                    raise Exception("El juego no existe")
                data['id_juego'] = juego.id
            if isinstance(data['id_juego'], dict):
                juego = models.Juego.objects.get(titulo=data['id_juego']['titulo'])
                if juego == None:
                    raise Exception("El juego no existe")
                data['id_juego'] = juego.id
        
        serializer = self.serializer_class(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=STATUS['CREATED'])
        
        return Response(serializer.errors, status=STATUS['BAD_REQUEST'])
    
    def partial_update(self, request, pk=None):
        queryset = self.model_class.objects.get(pk=pk)
        data = request.data
        
        #red social
        if 'id_red_social' in data and not isinstance(data['id_red_social'], int):
            if isinstance(data['id_red_social'], str):
                red_social, created = models.Red_social.objects.get_or_create(nombre=data['id_red_social'])
                data['id_red_social'] = red_social.id
            if isinstance(data['id_red_social'], dict):
                red_social, created = models.Red_social.objects.get_or_create(nombre=data['id_red_social']['nombre'], url=data['id_red_social']['url'])
                data['id_red_social'] = red_social.id
                
        #usuario
        if 'id_usuario' in data and not isinstance(data['id_usuario'], int):
            if isinstance(data['id_usuario'], str):
                usuario = models.Usuario.objects.get(nick=data['id_usuario'])
                if usuario == None:
                    raise Exception('No se encuentra el usuario')
                data['id_usuario'] = usuario.id
            if isinstance(data['id_usuario'], dict):
                usuario = models.Usuario.objects.get(nick=data['id_usuario']['nick'])
                if usuario == None:
                    raise Exception('No se encuentra el usuario')
                data['id_usuario'] = usuario.id
                
        #juego
        if 'id_juego' in data and not isinstance(data['id_juego'], int):
            if isinstance(data['id_juego'], str):
                juego = models.Juego.objects.get(titulo=data['id_juego'])
                if juego == None:
                    raise Exception("El juego no existe")
                data['id_juego'] = juego.id
            if isinstance(data['id_juego'], dict):
                juego = models.Juego.objects.get(titulo=data['id_juego']['titulo'])
                if juego == None:
                    raise Exception("El juego no existe")
                data['id_juego'] = juego.id
        
        serializer = self.serializer_class(
            queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=STATUS['BAD_REQUEST'])
    
    def seed_metacritic_mensajes_data(self, request):
        METACRITIC_DATA = {
            'name': 'Metacritic',
            'url': 'metacritic.com'
        }
        # self.model_class.objects.all().delete()
        form = forms.BuscarMensaje(request.POST or None)

        if form.is_valid():
            id_juego = form.cleaned_data['id_juego']
            
        juego = models.Juego.objects.get(pk=id_juego)
        metacritic_red_social = models.Red_social.objects.filter(
            Q(nombre=METACRITIC_DATA['name']) | Q(url=METACRITIC_DATA['url'])
        ).get_or_create(nombre=METACRITIC_DATA['name'], url=METACRITIC_DATA['url'])
            
        self.model_class.objects.filter(id_juego=juego.id, id_red_social=metacritic_red_social.id).delete()
        
        with open(os.path.join(settings.BASE_DIR, 'datos', 'metacritic_game_user_comments.csv'), 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            mensajes = []
            
            for row in reader:
                if row['Title'] != juego.titulo:
                    continue
                
                usuario, _ = models.Usuario.objects.filter(
                    Q(nombre=row['Username']) | Q(nick=row['Username'])
                ).get_or_create(nombre=row['Username'], nick=row['Username'], email=row['Username'] + '@mail.com')
                
                juego, _ = models.Juego.objects.filter(
                    Q(titulo=row['Title']) | Q(id_plataforma=models.Plataforma.objects.get_or_create(nombre=row['Platform'])[0])
                ).get_or_create(
                    titulo=row['Title'], 
                    id_plataforma=models.Plataforma.objects.get_or_create(nombre=row['Platform'])[0]
                )
                    
                mensaje = models.Mensaje(
                    f_mensaje='1970-01-01',
                    texto=row['Comment'],
                    id_juego=juego,
                    id_usuario=usuario,
                    id_red_social=metacritic_red_social
                )
                mensajes.append(mensaje)
                
        self.model_class.objects.bulk_create(mensajes)
        
        return Response('Los mensajes se crearon correctamente en la base de datos')
    
    def seed_play_store_game_data(self, request):
        PLAY_STORE_GAME = {
            'name': 'play_store_games',
            'url': 'playstore.com',
            'platform': 'playstore'
        }
        
        play_store_red_social, _ = models.Red_social.objects.filter(
            Q(nombre=PLAY_STORE_GAME['name']) | Q(url=PLAY_STORE_GAME['url'])
        ).get_or_create(nombre=PLAY_STORE_GAME['name'], url=PLAY_STORE_GAME['url'])
        
        play_store_platform, _ = models.Plataforma.objects.get_or_create(nombre=PLAY_STORE_GAME['platform'])
        
        models.Mensaje.objects.filter(id_red_social=play_store_red_social.id).delete()
        
        with open(os.path.join(settings.BASE_DIR, 'datos', 'PlayStoreGameAppInfoReview.json'), 'r') as jsonfile:
            json_data = json.load(jsonfile)
            juegos_selected = []
            
            for _ in range(10):
                mensajes = []
                juego_key, juego_value = random.choice(list(json_data.items()))
                while juego_key in juegos_selected:
                    juego_key, juego_value = random.choice(list(json_data.items()))
                
                juegos_selected.append(juego_key)
                
                for i in range(10):
                    user_name = juego_value['reviews'][i]['userName']
                    comment = juego_value['reviews'][i]['content']
                    
                    user, _ = models.Usuario.objects.filter(
                        Q(nick=user_name) | Q(nombre=user_name)
                    ).get_or_create(nick=user_name, nombre=user_name)
                    
                    juego, _ = models.Juego.objects.get_or_create(titulo=juego_value['appInfo']['title'], id_plataforma=play_store_platform)
                    
                    mensaje = models.Mensaje(
                        f_mensaje='1970-01-01',
                        texto=comment,
                        id_usuario=user,
                        id_juego=juego,
                        id_red_social=play_store_red_social
                    )
                    mensajes.append(mensaje)
                    
                models.Mensaje.objects.bulk_create(mensajes)

            return Response('Los mensajes han sido cargados correctamente')
