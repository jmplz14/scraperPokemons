# scraperPokemons
Con la necesidad de obtener los ficheros zip que una pagina web nos brinda con los modelos 3d
de los pokemons del juego pokemon X y pokemon Y, he creado un pequeño script python para obtener estos. 

La pagina utilizada para descargar los ficheros es <https://www.models-resource.com/3ds/pokemonxy/>. La página tiene los pokemons en
distintas secciones segun su generacion y ademas tiene mas modelos del juego como pueden ser personajes. En nuestro caso solo nos interesan los pokemons.

imagen

Recoremos todos los divs que contengan pokemon descargando la imagen de este pokemon y accediendo al link de la pagina de dicho pokemon. 

imagen

como se ve en la imagen la pagina tienen un enlace para descargar el zip del pokemon y alguna informacion de este. Nos quedaremos algunos campos de informacion 
y descargaremos el archivo zip.

Al ejecutar todo el script nos genera las carpetas imagenes y archivosZips ademas de un archivo csv con el nombre datosPokemons.csv.

En la carpeta imagenes tendremos las imagenes de portada de los poquemons con su codigo como nombre.

Imagen

En archivosZips de igual manera tendremos los archivos zips de cada pokemon que contienen los modelos 3d. Estos archivos tambien tendran como nombre
el codigo del pokemon al que corresponde.

Por ultimoe el archivo csv contendra el codigo y nombre del pokemon, el tamaño del fichero zip y la sección a la que pertenece.

imagen

Al ejecutar el script nos dira por que seccion de todas la que tenemos vamos y cuantos pokemons de dicha seccion nos falta para terminar.

imagen
