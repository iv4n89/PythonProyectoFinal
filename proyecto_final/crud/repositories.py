from . import models, serializers, forms
from django.conf import settings
from django.db.models import Q
import csv
import json
import os
import random

class BaseRepository():
    '''
    Clase generica base para todos los CRUD en cada uno de los modelos.
    '''
    serializer_class = None #Clase serializadora para la actual vista generica
    model_class = None #Clase de modelo para la actual vista generica

    def list(self, data=None):
        '''
        Selecciona todos los elementos del modelo actual desde la base de datos, y los ofrece al usuario
        '''
        queryset = self.model_class.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return serializer.data

    def create(self, data):
        '''
        Crea un elemento del modelo en la base de datos
        '''
        model, _ = self.model_class.objects.get_or_create(**data)
        serializer = self.serializer_class(model)
        return False, serializer.data

    def retrieve(self, data=None, pk=None):
        '''
        Selecciona un unico elemento, por PK, del modelo desde la base de datos
        '''
        queryset = self.model_class.objects.get(pk=pk)
        serializer = self.serializer_class(queryset)
        return serializer.data

    def partial_update(self, data, pk=None):
        '''
        Parcialmente actualiza un modelo en la base de datos
        '''
        queryset = self.model_class.objects.get(pk=pk)
        serializer = self.serializer_class(
            queryset, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return False, serializer.data
        return True, serializer.errors

    def destroy(self, data, pk=None):
        '''
        Elimina un elemento en la base de datos, por PK
        '''
        queryset = self.model_class.objects.get(pk=pk)
        queryset.delete()
        return True
    
class PlataformaRepository(BaseRepository):
    model_class = models.Plataforma
    serializer_class = serializers.PlataformaSerializer
    
    def search(self, data):
        plataforma = self.model_class.objects.filter(
            Q(nombre=data['nombre'])
        )
        serialized = self.serializer_class(plataforma, many=True)
        return serialized.data
    
class JuegoRepository(BaseRepository):
    model_class = models.Juego
    serializer_class = serializers.JuegoSerializer
    
    def search(self, data):
        filters = Q()
        if 'titulo' in data:
            filters &= Q(titulo__contains=data['titulo'])
        if 'f_publicacion' in data:
            filters &= Q(f_publicacion=data['f_publicacion'])
        if 'id_plataforma' in data:
            if not isinstance(data['id_plataforma'], int):
                if isinstance(data['id_plataforma'], str):
                    plataforma = models.Plataforma.objects.get(nombre=data['id_plataforma'])
                    filters &= Q(id_plataforma=plataforma.id)
                if isinstance(data['id_plataforma'], dict):
                    plataforma = models.Plataforma.objects.get(**data['id_plataforma'])
                    filters &= Q(id_plataforma=plataforma.id)
            else:
                filters &= Q(id_plataforma=data['id_plataforma'])
        juegos = self.model_class.objects.filter(filters)
        serialized = self.serializer_class(juegos, many=True)
        return serialized.data
    
    def create(self, data):
        '''
        Sobre escritura del metodo create. Se introduce la posibilidad de enviar la plataforma como un numero (FK), un str o un dict (en los dos ulimos casos se buscara o creara si no existe)
        '''
        if not isinstance(data['id_plataforma'], int):
            if isinstance(data['id_plataforma'], str):
                plataforma, created = models.Plataforma.objects.get_or_create(nombre=data['id_plataforma'])
                data['id_plataforma'] = plataforma.id
            if isinstance(data['id_plataforma'], dict):
                plataforma, created = models.Plataforma.objects.get_or_create(nombre=data['id_plataforma']['nombre'])
                data['id_plataforma'] = plataforma.id
                        
        model, _ = self.model_class.objects.get_or_create(**data)
        serializer = self.serializer_class(model)
        return False, serializer.data

    
    def partial_update(self, data, pk=None):
        '''
        Sobre escritura del metodo partial_update. Se introduce la posibilidad de enviar la plataforma como un int (FK), un str o un dict (en los dos ultimos casos se buscara o creara si no existe)
        '''
        queryset = self.model_class.objects.get(pk=pk)
        
        if 'id_plataforma' in data and not isinstance(data['id_plataforma'], int):
            if isinstance(data['id_plataforma'], str):
                plataforma, created = models.Plataforma.objects.get_or_create(nombre=data['id_plataforma'])
                data['id_plataforma'] = plataforma.id
            if isinstance(data['id_plataforma'], dict):
                plataforma, crated = models.Plataforma.objects.get_or_create(nombre=data['id_plataforma']['nombre'])
                data['id_plataforma'] = plataforma.id
                
        serializer = self.serializer_class(
            queryset, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return False, serializer.data
        return True, serializer.errors
    
    def seed_data_base(self, data):
        '''
        Metodo para poblar la base de datos desde fichero csv provisto con el proyecto.
        Esto elimina todos los registros de la tabla Juegos antes de realizar el poblado de nuevo para la tabla
        '''
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

        return True
    
class RedSocialRepository(BaseRepository):
    model_class = models.Red_social
    serializer_class = serializers.RedSocialSerializer
    
    def search(self, data):
        filters = Q()
        if 'nombre' in data:
            filters &= Q(nombre__contains=data['nombre'])
        if 'url' in data:
            filters &= Q(url=data['url'])
        red_social = self.model_class.objects.filter(filters)
        serialized = self.serializer_class(red_social, many=True)
        return serialized.data
    
class UsuarioRepository(BaseRepository):
    model_class = models.Usuario
    serializer_class = serializers.UsuarioSerializer
    
    def search(self, data):
        filters = Q()
        if 'nombre' in data:
            filters &= Q(nombre__contains=data['nombre'])
        if 'nick' in data:
            filters &= Q(nick__contains=data['nick'])
        if 'email' in data:
            filters &= Q(email__contains=data['email'])
        usuarios = self.model_class.objects.filter(filters)
        serialized = self.serializer_class(usuarios, many=True)
        return serialized.data
    
class MensajeRepository(BaseRepository):
    model_class = models.Mensaje
    serializer_class = serializers.MensajeSerializer
    
    def search(self, data):
        filters = Q()
        if 'f_mensaje' in data:
            filters &= Q(f_mensaje=data['f_mensaje'])
        if 'id_usuario' in data:
            if not isinstance(data['id_usuario'], int):
                if isinstance(data['id_usuario'], str):
                    usuario = models.Usuario.objects.get(nick=data['id_usuario'])
                    filters &= Q(id_usuario=usuario.id)
                if isinstance(data['id_usuario'], dict):
                    usuario = models.Usuario.objects.get(**data['id_usuario'])
                    filters &= Q(id_usuario=usuario.id)
            else:
                filters &= Q(id_usuario=data['id_usuario'])
        if 'id_red_social' in data:
            if not isinstance(data['id_red_social'], int):
                if isinstance(data['id_red_social'], str):
                    red_social = models.Red_social.objects.get(nombre=data['id_red_social'])
                    filters &= Q(id_red_social=red_social.id)
                if isinstance(data['id_red_social'], dict):
                    red_social = models.Red_social.objects.get(**data['id_red_social'])
                    filters &= Q(id_red_social=red_social.id)
            else:
                filters &= Q(id_red_social=data['id_red_social'])
        if 'id_juego' in data:
            if not isinstance(data['id_juego'], int):
                if isinstance(data['id_juego'], str):
                    juego = models.Juego.objects.get(titulo=data['id_juego'])
                    filters &= Q(id_juego=juego.id)
                if isinstance(data['id_juego'], dict):
                    juego = models.Juego.objects.get(**data['id_juego'])
                    filters &= Q(id_juego=juego.id)
            else:
                filters &= Q(id_juego=data['id_juego'])
        mensajes = self.model_class.objects.filter(filters)
        serialized = self.serializer_class(mensajes, many=True)
        return serialized.data
    
    def create(self, data):
        '''
        Sobre escritura del metodo create. Se introduce la posibilidad de enviar red social, juego y usuario como int (FK), str o dict. En el caso de red social, si no existe se creara
        '''
        
        #red social
        if not isinstance(data['id_red_social'], int):
            if isinstance(data['id_red_social'], str):
                red_social, created = models.Red_social.objects.get_or_create(nombre=data['id_red_social'])
                data['id_red_social'] = red_social
            if isinstance(data['id_red_social'], dict):
                red_social, created = models.Red_social.objects.get_or_create(nombre=data['id_red_social']['nombre'], url=data['id_red_social']['url'])
                data['id_red_social'] = red_social
                
        #usuario
        if not isinstance(data['id_usuario'], int): #pregunta varias instancias ~ para not 
            if isinstance(data['id_usuario'], str):
                usuario = models.Usuario.objects.get(nick=data['id_usuario'])
                if usuario == None:
                    raise Exception('No se encuentra el usuario')
                data['id_usuario'] = usuario
            if isinstance(data['id_usuario'], dict):
                usuario = models.Usuario.objects.get(nick=data['id_usuario']['nick'])
                if usuario == None:
                    raise Exception('No se encuentra el usuario')
                data['id_usuario'] = usuario
                
        #juego
        if not isinstance(data['id_juego'], int):
            if isinstance(data['id_juego'], str):
                juego = models.Juego.objects.get(titulo=data['id_juego'])
                if juego == None:
                    raise Exception("El juego no existe")
                data['id_juego'] = juego
            if isinstance(data['id_juego'], dict):
                juego = models.Juego.objects.get(titulo=data['id_juego']['titulo'])
                if juego == None:
                    raise Exception("El juego no existe")
                data['id_juego'] = juego
        
        model, _ = self.model_class.objects.get_or_create(**data)
        serializer = self.serializer_class(model)
        return False, serializer.data
    
    def partial_update(self, data, pk=None):
        '''
        Sobre escritura para el metodo partial_update. Se introduce la posibilidad de enviar red social, juego y usuario como int (FK), str o dict. En el caso de red social, si no existe se creara
        '''
        queryset = self.model_class.objects.get(pk=pk)
        
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
            queryset, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return False, serializer.data
        return True, serializer.errors
    
    def seed_metacritic_mensajes_data(self, request):
        '''
        Metodo de poblacion de base de datos para la tabla mensajes, usando de base el fichero csv facilitado con el proyecto
        Este tomara el juego que se envia desde el request y buscara todos los mensajes y reviews enviados por usuarios, los cuales seran introducidos a la base de datos
        '''
        METACRITIC_DATA = {
            'name': 'Metacritic',
            'url': 'metacritic.com'
        }
        # self.model_class.objects.all().delete()
        form = forms.BuscarMensaje(request.POST or None)

        if form.is_valid():
            id_juego = form.cleaned_data['id_juego']
            
        juego = models.Juego.objects.get(pk=id_juego)
        metacritic_red_social, created = models.Red_social.objects.filter(
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
                    
                mensaje = models.Mensaje.factory(
                    texto=row['Comment'],
                    id_juego=juego,
                    id_usuario=usuario,
                    id_red_social=metacritic_red_social
                )
                mensajes.append(mensaje)
                
        self.model_class.objects.bulk_create(mensajes)
        
        return True
    
    def seed_play_store_game_data(self, request):
        '''
        Metodo de poblacion de la tabla mensajes, usando de base el fichero json que se facilita con el proyecto.
        Este seleccionara 10 juegos aleatorios de entre todos los disponibles, recogiendo todos los mensajes enviados por los usuarios para todos los 10 juegos seleccionados e introduciendo sus datos a la base de datos.
        Antes de la seleccion y posterior introduccions de datos a la base de datos, se borraran todos los mensajes que hayan sido registrados para la red social de playstore
        '''
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
                    
                    mensaje = models.Mensaje.factory(
                        texto=comment,
                        id_usuario=user,
                        id_juego=juego,
                        id_red_social=play_store_red_social
                    )
                    mensajes.append(mensaje)
                    
                models.Mensaje.objects.bulk_create(mensajes)

            return True