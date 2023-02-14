from rest_framework import serializers
from . import models

class JuegoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Juego
        fields = '__all__'
        
class RedSocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Red_social
        fields = '__all__'
        
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Usuario
        fields = '__all__'
        
class MensajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Mensaje
        fields = '__all__'