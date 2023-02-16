from rest_framework import viewsets
from rest_framework.response import Response
import csv
from . import models
from . import serializers
import os
from django.conf import settings

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
