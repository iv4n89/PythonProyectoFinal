from django.db import models
from django.utils import timezone

# Create your models here.
class Plataforma(models.Model):
    nombre = models.CharField(max_length=100)

class Juego(models.Model):
    tit_juego = models.CharField(max_length=120)
    plataforma = models.ForeignKey(Plataforma, on_delete=models.CASCADE)
    f_publicacion = models.IntegerField()
    
class Red_social(models.Model):
    rom_red_social = models.CharField(max_length=45)
    url_red_social = models.CharField(max_length=150)
    
class Usuario(models.Model):
    nick_usuario = models.CharField(max_length=45)
    nom_usuario = models.CharField(max_length=120)
    email_usuario = models.CharField(max_length=120)
    
class Mensaje(models.Model):
    f_mensaje = models.DateField(default=timezone.now)
    text_mensaje = models.CharField(max_length=250)
    id_juego = models.ForeignKey(Juego, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_red_social = models.ForeignKey(Red_social, on_delete=models.CASCADE)
