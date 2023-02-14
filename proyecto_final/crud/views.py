from rest_framework import viewsets
from rest_framework.response import Response
from . import models
from . import serializers

STATUS = {
    'OK': 200,
    'CREATED': 201,
    'NO_CONTENT': 204,
    'BAD_REQUEST': 400,
    'NOT_FOUND': 404,
}

# Create your views here.
# Juego

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
        serializer = self.serializer_class(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=STATUS['BAD_REQUEST'])
    
    def destroy(self, request, pk=None):
        queryset = self.model_class.objects.get(pk=pk)
        queryset.delete()
        return Response(status=STATUS['NO_CONTENT'])
    
    
class JuegoViewSet(BaseViewSet):
    model_class = models.Juego
    serializer_class = serializers.JuegoSerializer
    
class RedSocialViewSet(BaseViewSet):
    model_class = models.Red_social
    serializer_class = serializers.RedSocialSerializer
    
class UsuarioViewSet(BaseViewSet):
    model_class = models.Usuario
    serializer_class = serializers.UsuarioSerializer
    
class MensajeViewSet(BaseViewSet):
    model_class = models.Mensaje
    serializer_class = serializers.MensajeSerializer