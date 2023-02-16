from django.db import models
from django.utils import timezone

# Create your models here.
class Plataforma(models.Model):
    nombre = models.CharField(max_length=100, unique=True, null=False, default='')

class Juego(models.Model):
    titulo = models.CharField(max_length=120, null=False, default='')
    id_plataforma = models.ForeignKey(Plataforma, on_delete=models.CASCADE)
    f_publicacion = models.IntegerField()
    
class Red_social(models.Model):
    nombre = models.CharField(max_length=45, unique=True, null=False, default='')
    url = models.CharField(max_length=150)
    
class Usuario(models.Model):
    nick = models.CharField(max_length=45, unique=True, null=False, default='')
    nombre = models.CharField(max_length=120)
    email = models.CharField(max_length=120)
    
class Mensaje(models.Model):
    f_mensaje = models.DateField(default=timezone.now)
    texto = models.CharField(max_length=250)
    id_juego = models.ForeignKey(Juego, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_red_social = models.ForeignKey(Red_social, on_delete=models.CASCADE)
