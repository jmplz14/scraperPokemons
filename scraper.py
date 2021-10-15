import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from io import BytesIO
from zipfile import ZipFile
from os.path  import basename

web = "https://www.models-resource.com"
link = web + "/3ds/pokemonxy/"
#link_inicio = web + "/3ds/pokemonxy/model/9318/"
#link_fin = web + "/3ds/pokemonxy/model/9318/"

def descargar_y_descomprimir_zip(enlace, destino='.'):
    http_response = urlopen(enlace)
    zipfile = ZipFile(BytesIO(http_response.read()))
    zipfile.extractall(path=destino)

def obtener_html(enlace):
    try:
        r = requests.get(enlace)
        soup = BeautifulSoup(r.text, "html.parser")
        return soup
    except requests.exceptions.Timeout:
        print("La peticion ha caducado")
        # Maybe set up for a retry, or continue in a retry loop
        exit(1)
    except requests.exceptions.TooManyRedirects:
        print("Url erronea")
        exit(1)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)


def obtener_datos_pokemon(soup):
    datos = {}
    tabla = soup.find("div", {"id": "game-info-wrapper"})
    columnas = tabla.find_all("tr")

    datos_pokemon = columnas[0].find("th").find("div").text
    datos_pokemon = datos_pokemon.split()
    
    datos["codigo"] = datos_pokemon[0]
    datos["nombre"] = datos_pokemon[1]
    datos["tamaño"] = columnas[5].find_all("td")[1].text
    datos["zip"] = columnas[9].find("a").get("href")
    datos["seccion"] = columnas[3].find_all("td")[1].text
    datos["siguiente"] =   soup.find_all(
        "a", {"href": re.compile("/3ds/pokemonxy/model*")})[4].get("href")
    siguiente = soup.find_all(
        "a", {"href": re.compile("/3ds/pokemonxy/model*")})
    #print(siguiente)
    return datos

soup = obtener_html(link)
secciones = soup.find_all("div", {"class": "updatesheeticons"})

#def descargar_imagen():

def descargar_imagen(enlace,nombre):

    with open("imagenes/" + nombre + ".png" , "wb") as f:
        f.write(requests.get(enlace).content)



for i in range(0,1):

    pokemons = secciones[i].find_all("a")

    for pokemon in pokemons:

        html_pokemon = obtener_html(web + pokemon.get("href"))
        datos = obtener_datos_pokemon(html_pokemon)

        imagen =  pokemon.find("div", {"class": "iconbody"})
        imagen = imagen.find("img").get("src")
        datos["imagen"] = imagen

        descargar_imagen(web+imagen, datos["codigo"])
        descargar_y_descomprimir_zip(web + datos["zip"])

        print(datos)
    



"""soup = obtener_html(link_inicio)

parada = True
while parada:
    datos = obtener_datos_pokemon(soup)
    print(datos)
    descargar_y_descomprimir(web + datos["zip"])
    nuevo_link = web + datos["siguiente"]
    soup = obtener_html(web + datos["siguiente"])
"""
    




# print(siguiente[4].get("href"))

#funcion  para sumar los n primeros pares