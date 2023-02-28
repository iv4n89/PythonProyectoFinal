from rest_framework import viewsets
from rest_framework.response import Response
from . import repositories


STATUS = {
    'OK': 200,
    'CREATED': 201,
    'NO_CONTENT': 204,
    'BAD_REQUEST': 400,
    'NOT_FOUND': 404,
}

class BaseViewSet(viewsets.ViewSet):
    '''
    Clase generica base para todos los CRUD en cada uno de los modelos.
    '''
    repository = None

    def list(self, request):
        '''
        Selecciona todos los elementos del modelo actual desde la base de datos, y los ofrece al usuario
        '''
        data = self.repository.list(request.data)
        return Response(data)

    def create(self, request):
        '''
        Crea un elemento del modelo en la base de datos
        '''
        errors, data = self.repository.create(request.data)
        print(data)
        if errors:
            return Response(data, status=STATUS['BAD_REQUEST'])
        return Response(data, status=STATUS['CREATED'])

    def retrieve(self, request, pk=None):
        '''
        Selecciona un unico elemento, por PK, del modelo desde la base de datos
        '''
        data = self.repository.retrieve(request.data, pk)
        return Response(data)

    def partial_update(self, request, pk=None):
        '''
        Parcialmente actualiza un modelo en la base de datos
        '''
        errors, data = self.repository.partial_update(request.data, pk)
        if errors:
            return Response(data, status=STATUS['BAD_REQUEST'])
        return Response(data, status=STATUS['OK'])
    
    def search(self, request):
        data = self.repository.search(request.data)
        return Response(data)

    def destroy(self, request, pk=None):
        '''
        Elimina un elemento en la base de datos, por PK
        '''
        self.repository.destroy(request.data, pk)
        return Response(status=STATUS['NO_CONTENT'])

class PlataformaViewSet(BaseViewSet):
    '''
    Vistas para formar el CRUD para el modelo Plataforma
    '''
    repository = repositories.PlataformaRepository()
        

class JuegoViewSet(BaseViewSet):
    '''
    Vistas para formar el CRUD para el modelo Juego
    '''
    repository = repositories.JuegoRepository()
        
    def seed_data_base(self, request):
        '''
        Metodo para poblar la base de datos desde fichero csv provisto con el proyecto.
        Esto elimina todos los registros de la tabla Juegos antes de realizar el poblado de nuevo para la tabla
        '''
        result = self.repository.seed_data_base(request.data)

        if result:
            return Response('Los juegos se cargaron correctamente desde el csv')
        return Response('Algo salio mal')


class RedSocialViewSet(BaseViewSet):
    '''
    Vistas para formar el CRUD del modelo Red Social
    '''
    repository = repositories.RedSocialRepository()
    

class UsuarioViewSet(BaseViewSet):
    '''
    Vistas para formar el CRUD del modelo Usuario
    '''
    repository = repositories.UsuarioRepository()


class MensajeViewSet(BaseViewSet):
    '''
    Vistas para formar el CRUD del modelo Mensaje
    '''
    repository = repositories.MensajeRepository()
    
    def quantity_per_user(self, request):
        
        messages = self.repository.quantity_per_user()
        return Response(messages)
    
    def seed_metacritic_mensajes_data(self, request):
        '''
        Metodo de poblacion de base de datos para la tabla mensajes, usando de base el fichero csv facilitado con el proyecto
        Este tomara el juego que se envia desde el request y buscara todos los mensajes y reviews enviados por usuarios, los cuales seran introducidos a la base de datos
        '''
        data = request.data
        result = self.repository.seed_metacritic_mensajes_data(data=data)
        
        if result:
            return Response('Los mensajes se crearon correctamente en la base de datos')
        return Response('Algo salio mal')
    
    def seed_play_store_game_data(self, request):
        '''
        Metodo de poblacion de la tabla mensajes, usando de base el fichero json que se facilita con el proyecto.
        Este seleccionara 10 juegos aleatorios de entre todos los disponibles, recogiendo todos los mensajes enviados por los usuarios para todos los 10 juegos seleccionados e introduciendo sus datos a la base de datos.
        Antes de la seleccion y posterior introduccions de datos a la base de datos, se borraran todos los mensajes que hayan sido registrados para la red social de playstore
        '''
        result = self.repository.seed_play_store_game_data(request)

        if result:
            return Response('Los mensajes han sido cargados correctamente')
        return Response('Algo salio mal')
