# Proyecto final Python Ivan Betanzos Macias

## Antes de empezar
Será necesario añadir al proyecto la base de datos y los ficheros de la carpeta datos. Para ello, se hará lo siguiente:

- Crear un fichero llamado __*db.sqlite*__ dentro de la carpeta __db__
- Copiar los 3 ficheros de la carpeta __datos__

Se creará a mano el fichero __*db.sqlite*__ de cara a poder tener los cambios fuera del contenedor.

<br>

## Levantar el contenedor y lanzar el proyecto

Para levantar el contenedor de django lanzaremos el siguiente comando, desde la raiz de la aplicación:

> docker-compose up

Esto es si queremos tener los logs en la consola de comandos. <br>
Si no necesitamos los logs, lanzaremos el comando:

> docker-compose up -d

Esto realizará:

- Contruye el contenedor de Docker
- Copia el proyecto dentro del contenedor
- Lanza el migrate de django
- Inicia el proyecto en 0.0.0.0:8000 (accesible desde localhost:8000)

Desde este momento será posible acceder a la aplicación, ya en funcionamiento

<br>

## Dentro de la aplicación

Una vez en la aplicación web, tendremos como bienvenida una serie de botones para cargar la base de datos. <br>
Es importante en este punto tener los ficheros de la carpeta __datos__ en el proyecto. En caso de no haberse incluido antes de realizar el build del contenedor, se podrá añadir en cualquier momento, ya que tenemos la carpeta linkeada como volumen del contenedor
<br>

Se podrá realizar las siguientes acciones con los botones que tenemos en la página:

- Recargar juegos db: Se cargarán los juegos desde el csv, hacia la base de datos
- Recargar mensajes metacritic juego: Nos llevará a la vista de Lista de juegos. Seleccionando un juego, se cargarán los mensajes de metacritic desde el csv para el juego seleccionado.
- Recargar mensajes google play store: Se cargarán, desde el fichero json, los mensajes de 10 juegos al azar. Se podrán encontrar los juegos cargados al final de la lista de juegos. Los mensajes se visualizarán clicando en el juego.
- Lanzar spider: Esto lanzará el spider de Scrapy. Para ver los mensajes cargados podemos ir a la vista de Lista de juegos, e ir abajo del todo. Encontraremos el juego Roboquest, que es el juego del que se ha realizado scraping en Steam. Además de esto, podemos pulsar en el botón Scraping a Steam para ver los mensajes traídos por el spider.

<br>

## Consultas del proyecto

Las 4 consultas que se piden para el proyecto se encontrarán en los botones arriba. Con los siguientes nombres:

- Mensajes por usuario
- Formulario apariciones en mensajes
- Formulario media mensajes
- Se habla mas en...

<br>


### Proyecto realizado por Iván Betanzos Macías
#### Curso Python 2022-2023

<hr>

#### Github 
> https://github.com/iv4n89/PythonProyectoFinal