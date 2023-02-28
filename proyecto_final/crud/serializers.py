from rest_framework import serializers
from . import models

class PlataformaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Plataforma
        fields = '__all__'

class JuegoSerializer(serializers.ModelSerializer):
    id_plataforma = PlataformaSerializer()
    class Meta:
        model = models.Juego
        fields = ['titulo', 'id_plataforma', 'f_publicacion', 'id']
        
class RedSocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Red_social
        fields = '__all__'
        
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Usuario
        fields = '__all__'
        
class MensajeSerializer(serializers.ModelSerializer):
    id_juego = JuegoSerializer()
    id_red_social = RedSocialSerializer()
    id_usuario = UsuarioSerializer()
    class Meta:
        model = models.Mensaje
        fields = '__all__'