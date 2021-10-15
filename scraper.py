import requests
import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import os
from io import BytesIO
from zipfile import ZipFile


web = "https://www.models-resource.com"
link = web + "/3ds/pokemonxy/"


# Se encarga de descargar el fichero zip y guardarlo
def descargar_zip(enlace, nombre):
    r = requests.get(enlace, stream=True)
    with open("archivosZips/" + nombre + ".zip", 'wb') as fd:
        for chunk in r.iter_content(chunk_size=128):
            fd.write(chunk)


# Obtiene el codigo html que usaremos para obtener datos
def obtener_html(enlace):
    # Comprobamos errores a la hora de obtener el html
    try:
        r = requests.get(enlace)
        soup = BeautifulSoup(r.text, "html.parser")
        return soup
    except requests.exceptions.Timeout:
        print("Error: La peticion ha caducado")
        exit(1)
    except requests.exceptions.TooManyRedirects:
        print("Error: Url erronea")
        exit(1)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

# Esta función nos da los datos de un pokemon


def obtener_datos_pokemon(soup):

    datos = {}

    # Nos quedamos la tabla y despues las columnas donde esta la información
    tabla = soup.find("div", {"id": "game-info-wrapper"})
    columnas = tabla.find_all("tr")

    # Obtenemos el nombre y código del pokemon
    datos_pokemon = columnas[0].find("th").find("div").text
    datos_pokemon = datos_pokemon.split()
    datos["codigo"] = datos_pokemon[0]
    datos["nombre"] = datos_pokemon[1]

    # guardamos el tamaño, el enlace del fichero zip y la sección
    datos["tamaño"] = columnas[5].find_all("td")[1].text
    datos["zip"] = columnas[9].find("a").get("href")
    datos["seccion"] = columnas[3].find_all("td")[1].text

    return datos

# Descarga y guarda la imagen en la carpeta


def descargar_imagen(enlace, nombre):
    with open("imagenes/" + nombre + ".png", "wb") as f:
        f.write(requests.get(enlace).content)

# Crea una carpeta y comprueba que no se de un error


def crear_carpeta(nombre):
    try:
        os.mkdir(nombre)
    except OSError:
        print("Error al crear la carpeta" + nombre)
        exit(1)


crear_carpeta("imagenes")
crear_carpeta("archivosZips")

# obtenemos el html y nos quedamos con las secciones que tienen elementos con modelos 3d
soup = obtener_html(link)
secciones = soup.find_all("div", {"class": "updatesheeticons"})

#abrimos el fichero csv y le añadimos la cabecera
fichero_datos = open("datosPokemons.csv", "w")
fichero_datos.write("Código,Nombre,Tamaño,Sección" + os.linesep)

#recorremos las secciones que tienen pokemons
for i in range(1, 7):

    #nos quedamos la parte del html que contiene la imagen y enlace a la pagina de los pokemon
    pokemons = secciones[i].find_all("a")

    total_pokemons = len(pokemons)
    num_pokemon = 0
    #recorremos todos los pokemos de esta seccion
    for pokemon in pokemons:

        #obtenemos el html de la página de cada pokemons y sus datos
        html_pokemon = obtener_html(web + pokemon.get("href"))
        datos = obtener_datos_pokemon(html_pokemon)

        #Obtenemos el enlace a la imagen y lo guardamos
        imagen = pokemon.find("div", {"class": "iconbody"})
        imagen = imagen.find("img").get("src")
        datos["imagen"] = imagen

        #descargamos la imagen y el zip 
        descargar_imagen(web+imagen, datos["codigo"])
        descargar_zip(web + datos["zip"], datos["codigo"])
        
        #creamos la linea del csv correspondiente y la escribimos en el fichero
        csv_linea = datos["codigo"] + "," + datos["nombre"] + \
            "," + datos["tamaño"] + "," + datos["seccion"]
        fichero_datos.write(csv_linea + os.linesep)


        num_pokemon += 1
        #mostramos el mensaje que nos muestra por que sección y pokemon vamos
        print("Descargado %s perteneciente a la sección %s que es la %dº de 6 secciones. Pokemon %dº de %d de esta sección " % (
            datos["codigo"] + " " + datos["nombre"], datos["seccion"], i, num_pokemon, total_pokemons))

#Cerramos el fichero csv
fichero_datos.close()
