import scrapy
from .. import items


class AmazonGamesSpider(scrapy.Spider):
    name = "amazon_games"
    allowed_domains = ["amazon.es"]
    start_urls = ["https://steamcommunity.com/app/692890/reviews/?browsefilter=toprated&snr=1_5_100010_"]

    def parse(self, response):
        title = response.css('div.apphub_AppName ::text').extract_first()
        comments = response.css('div.apphub_Card.modalContentLink.interactable')
        
        for comment in comments:
            plataforma = items.PlataformaItem()
            plataforma.nombre = 'PC'
            red_social = items.RedSocialItem()
            red_social.nombre = 'Steam'
            red_social.url = 'steamcommunity.com'
            juego = items.JuegoItem()
            juego.titulo = title
            juego.id_plataforma = plataforma
            mensaje = items.MensajeItem()
            usuario = items.UsuarioItem()
            
            text = comment.xpath('//div[@class="apphub_CardTextContent"]/text()').extract_first()
            user = comment.css('div.apphub_CardContentAuthorName ::text').extract_first()
            date = comment.css('div.date_posted ::text').extract_first()[8:]
            
            usuario.nombre = user
            usuario.nick = user
            
            mensaje.texto = text
            mensaje.id_usuario = usuario
            mensaje.f_mensaje = date
            mensaje.id_red_social = red_social
            mensaje.id_juego = juego
            print(plataforma)
