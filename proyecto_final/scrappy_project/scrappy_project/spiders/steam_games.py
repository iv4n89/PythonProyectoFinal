import scrapy, re
from .. import items
from datetime import datetime
from crud import repositories



class SteamGamesSpider(scrapy.Spider):
    name = "steam_games"
    allowed_domains = ["steamcommuntity.com"]
    start_urls = ["https://steamcommunity.com/app/692890/reviews/"]
    
    API_CREATE_MENSAJE = 'http://127.0.0.1:8000/api/mensaje/create'

    def parse(self, response):
        title = response.css('div.apphub_AppName ::text').extract_first()
        comments = response.css('div.apphub_Card.modalContentLink.interactable')
        print(title)
        
        for i in range(len(comments)):
            plataforma = items.PlataformaItem()
            plataforma['nombre'] = 'PC'
            _, plataforma = repositories.PlataformaRepository().create(plataforma)
            red_social = items.RedSocialItem()
            red_social['nombre'] = 'Steam'
            red_social['url'] = 'steamcommunity.com'
            _, red_social = repositories.RedSocialRepository().create(red_social)
            juego = items.JuegoItem()
            juego['titulo'] = title
            juego['id_plataforma'] = plataforma
            _, juego = repositories.JuegoRepository().create(juego)
            mensaje = items.MensajeItem()
            usuario = items.UsuarioItem()
            
            text = comments[i].xpath('//div[@class="apphub_CardTextContent"]').extract()[i]
            text_start_index = re.search(r'<br>', text).end()
            text = text[text_start_index:]
            text_end_index = re.search(r'</div>', text).start()
            text = text[:text_end_index].strip()
            user = comments[i].css('div.apphub_CardContentAuthorName ::text').extract_first()
            date = comments[i].css('div.date_posted ::text').extract_first()[8:]
            date = date_conversion(date)
            
            _, usuario = repositories.UsuarioRepository().create({"nombre": user, "nick": user})
            
            mensaje['texto'] = text
            mensaje['id_usuario'] = usuario
            mensaje['f_mensaje'] = date
            mensaje['id_red_social'] = red_social
            mensaje['id_juego'] = juego
            
            _, mensaje = repositories.MensajeRepository().create(mensaje)
            
            yield mensaje

def date_conversion(date: str):
    MONTHS = {
        'January': '1',
        'February': '2',
        'March': '3',
        'April': '4',
        'May': '5',
        'June': '6',
        'July': '7',
        'August': '8',
        'September': '9',
        'October': '10',
        'November': '11',
        'December': '12'
    }
    
    date_splitted = date.split(' ')
    
    date_splitted[1] = MONTHS[date_splitted[1]]
    
    if len(date_splitted) == 2:
        date_splitted.append(str(datetime.now().year))
        
    date_splitted.reverse()
    
    return '-'.join(date_splitted)