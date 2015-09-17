#!/usr/bin/python
# -*- coding: utf-8 -*-
from AnalisisLinguistico.AnalisisMorfologico import *
from ServiciosTecnicos.GestorEntradasSalidas import *

def obtenerEntidadesFuerzaBruta(texto, entidadesConocidas):
    # identifica las entidades en un texto* (texto es un vector de textos) basandose en
    # una lista de entidades conocidas. comprueba en cada palabra si corresponde a una entidad.

    # limitaciones:
    # no reconoce el nombre completo cuando presenta una abreviatura en medio

    contadorArt=0
    nombresPorArticulo = []
    for articulo in texto:
        nombresArticuloX = []

        palabras = articulo.split()

        nombreCompleto=False
        constructorNombre= ""
        nroNombresCostruc = 0
        nroPalabra=1
        for palabra in palabras:
            #evita no reconocer una entidad por tener puntuacion
            if palabra.__contains__("."):
                palabra = palabra.replace(".","")
                nombreCompleto=True
            if palabra.__contains__(","):
                palabra = palabra.replace(",","")
                nombreCompleto=True

            # La entidad continua hasta que se encuentra con una noEntidad
            esNombre=False
            for nombre in entidadesConocidas:
                if palabra == nombre:
                    esNombre =True
                    constructorNombre = constructorNombre+" "+palabra
                    nroNombresCostruc = nroNombresCostruc+1
                    break
            if not esNombre:
                nombreCompleto=True
            if nombreCompleto:
                if nroNombresCostruc <> 0:
                    if nroNombresCostruc > 1:       #filtra por un nro minimo de entidades contiguas
                        nombresArticuloX.append(constructorNombre)
                        nombresArticuloX.append(nroPalabra)
                    constructorNombre = ""
                    nroNombresCostruc=0
                nombreCompleto=False
            nroPalabra= nroPalabra+1
        nombresPorArticulo.append(nombresArticuloX)
        contadorArt =contadorArt+1
        if contadorArt ==5:
            break
    cont =1
    for nombreArtX in nombresPorArticulo:
        print texto[cont-1]
        print cont, nombreArtX, "\n"*2
        cont = cont+1


def getEntidadesMayusConConecteres(texto, entidadesConocidas, conectoresEntidad):
    # identifica las entidades en un texto* (texto es un vector de textos) basandose en
    # una lista de entidades conocidas. Una vez encuentra una entidad, si la siguiente palabra comienza con mayus
    # entonces tambien es una entidad.
    # Posee tambien la posibilidad de agregar palabras conectoras, esto permite que por ejemplo
    # se reconozca "Juana de la rosa" como entidad si "de" y "la" son conectoresEntidad

    # limitaciones:
    # no reconoce el nombre completo cuando presenta una abreviatura en medio
    # Problemas al no finalizar conexion. Ej. "Durante la" (porque durante es un apellido) articulo 2

    contadorArt=0
    nombresPorArticulo = []
    for articulo in texto:
        nombresArticuloX = []
        palabras = articulo.split()

        constructorNombre= ""
        nroNombresCostruc = 0
        nroPalabra=1

        estoyEnUnNombre = False
        finalizadaConexion = True
        palabraConectora=False
        for palabra in palabras:

            #evita no reconocer una entidad por tener puntuacion
            palabraPuntuada=False
            if palabra.__contains__("."):
                palabra = palabra.replace(".","")
                palabraPuntuada=True
            if palabra.__contains__(","):
                palabra = palabra.replace(",","")
                palabraPuntuada=True

            # detecta si palabra es una entidad conectora
            #if palabraConectora and not conectoresEntidad.__contains__(palabra):            #MEJORAR, CODIGO HORRIBLE
                #finalizadaConexion= True
            palabraConectora=False
            if conectoresEntidad.__contains__(palabra):
                palabraConectora=True

            # La entidad continua hasta que se encuentra con una noEntidad
            if not estoyEnUnNombre:
                for nombre in entidadesConocidas:
                    #palabra = str(palabra)
                    if palabra == nombre:
                        estoyEnUnNombre=True
                        break
            if estoyEnUnNombre:
                if palabra[0].isupper() or palabraConectora:
                    constructorNombre = constructorNombre+" "+palabra
                    nroNombresCostruc = nroNombresCostruc+1

                if (not palabra[0].isupper() or palabraPuntuada) and not palabraConectora: #and finalizadaConexion:
                    estoyEnUnNombre = False
                    if nroNombresCostruc <> 0:    # filtrado: si no tiene entidades no agregue
                        if nroNombresCostruc > 1: # filtrado: por un nro minimo de entidades contiguas
                            nombresArticuloX.append(constructorNombre)
                            nombresArticuloX.append(nroPalabra)
                        constructorNombre = ""
                        nroNombresCostruc=0
            nroPalabra= nroPalabra+1
        nombresPorArticulo.append(nombresArticuloX)
        contadorArt =contadorArt+1
        if contadorArt ==5:                 # para que lea solo los primeros 5 articulos
            break

    #Muestro los resultados.
    cont =1
    for nombresArtX in nombresPorArticulo:
        print cont, "\n", texto[cont-1]
        for nombre in nombresArtX:
            print nombre
        print "\n"*2
        cont = cont+1

def getEntidadesMayus(texto, entidadesConocidas, conectoresEntidad):
    # identifica las entidades en un texto* (texto es un vector de textos) basandose en
    # una lista de entidades conocidas. Una vez encuentra una entidad, si la siguiente palabra comienza con mayus
    # entonces tambien es una entidad.
    # Posee tambien la posibilidad de agregar palabras conectoras, esto permite que por ejemplo
    # se reconozca "Juana de la rosa" como entidad si "de" y "la" son conectoresEntidad

    # limitaciones:
    # no reconoce el nombre completo cuando presenta una abreviatura en medio
    # Problemas al no finalizar conexion. Ej. "Durante la" (porque durante es un apellido) articulo 2
    marcaNegritaI = "<br>"
    marcaNegritaF = "</br>"
    marcaNombres  = "#"

    contadorArt=0
    nombresPorArticulo = []
    articulosMarcados = []
    for articulo in texto:
        articulosMarcados.append("")
        nombresArticuloX = []
        palabras = articulo.split()

        constructorNombre= ""
        nroNombresCostruc = 0
        nroPalabra=1

        estoyEnUnNombre = False
        for palabra in palabras:
            estabaEnUnNombre = False
            #evita no reconocer una entidad por tener puntuacion
            palabraPuntuada=False
            if palabra.__contains__("."):
                palabra = palabra.replace(".","")
                palabraPuntuada=True
            if palabra.__contains__(","):
                palabra = palabra.replace(",","")
                palabraPuntuada=True

            # detecta si palabra es una entidad conectora
            palabraConectora=False
            if conectoresEntidad.__contains__(palabra):
                palabraConectora=True

            # La entidad continua hasta que se encuentra con una noEntidad
            if not estoyEnUnNombre:
                for nombre in entidadesConocidas:
                    #palabra = str(palabra)
                    if palabra == nombre:
                        estoyEnUnNombre=True
                        break
            if estoyEnUnNombre:
                if palabra[0].isupper() or palabraConectora:
                    constructorNombre = constructorNombre+" "+palabra
                    nroNombresCostruc = nroNombresCostruc+1

                # detecta si acabo la entidad
                if (not palabra[0].isupper() or palabraPuntuada) and not palabraConectora: #and finalizadaConexion:
                    estoyEnUnNombre = False
                    if nroNombresCostruc <> 0:    # filtrado: si no tiene entidades no agregue
                        if nroNombresCostruc > 1: # filtrado: por un nro minimo de entidades contiguas, Agrega entidad
                            nombresArticuloX.append(constructorNombre)
                            entidad = marcaNegritaI+constructorNombre+" "+marcaNegritaF
                            articulosMarcados[contadorArt] += entidad+" "
                            #ArticulosMarcados[contadorArt] = ArticulosMarcados[contadorArt]+palabra
                        constructorNombre = ""
                        nroNombresCostruc=0
            else:
                articulosMarcados[contadorArt] += palabra+" "
        nombresPorArticulo.append(nombresArticuloX)
        contadorArt =contadorArt+1
        if contadorArt ==5:                 # para que lea solo los primeros 5 articulos
            break
    #return articulosMarcados, nombresPorArticulo

    #Muestro los resultados.
    for cont in range(len(nombresPorArticulo)):
        #print cont+1, "\n", texto[cont], \
        print "\n"*2, "CON MARCAS", "\n"*2, articulosMarcados[cont], "\n"
        nombresArtX = nombresPorArticulo[cont]
        print marcaNombres.join(nombresArtX)


#Main

archivoNombres = "Names.xls"
nombres=   cargarColumnaEnLista(archivoNombres,0,0,1,3500)
apellidos= cargarColumnaEnLista(archivoNombres,1,0,1,3500)
listaNombresApellidos =nombres+apellidos
archivoNoticias = "39Art.txt"
noticias = cargarcsv(archivoNoticias, "#")

conectoresNombres = "de,del,los,la,las,y".split(",")

#obtenerEntidadesFuerzaBruta(noticias,listaNombresApellidos)
getEntidadesMayus(noticias,listaNombresApellidos,conectoresNombres)



# Dataframe pandas en pycharm
# Arreglar el metodo de conectores. Conexion final.



#problemas con la base de datos de nombres
    # contiene cosas que no son nombres o apellidos: "Gastos varios"
    # La seccion de apellidos tiene nombres y apellidos en una misma linea
    # añadir nombres con tildes. josé no lo reconoce
#problemas con la base de datos de noticias
    # luego de una coma no ponene espacio luego, en Vaupés,Fabio Arango Torres, solo reconoce, Arango Torres

#Problemas sin solución
# reconoce entidades que no son nombres o apellidos.


#Hallazgos:
# los nombres aislados son utiles para encontrar palabras que no estan en la BD de nombres.
# Los alias son facilmente encontrados por las comillas.




