# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy_djangoitem import DjangoItem
from crud import models

class PlataformaItem(DjangoItem):
    django_model = models.Plataforma

class JuegoItem(DjangoItem):
    django_model = models.Juego
    
class RedSocialItem(DjangoItem):
    django_model = models.Red_social
    
class UsuarioItem(DjangoItem):
    django_model = models.Usuario
    
class MensajeItem(DjangoItem):
    django_model = models.Mensaje
