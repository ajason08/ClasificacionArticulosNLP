#!/usr/bin/python
# -*- coding: utf-8 -*-
from AnalisisLinguistico.AnalisisMorfologico import *
from ServiciosTecnicos.GestorEntradasSalidas import *

archivoNombres = "Names.xls"
nombres=   cargarColumnaEnLista(archivoNombres,0,0,1,3500)
apellidos= cargarColumnaEnLista(archivoNombres,1,0,1,3500)
nombresApellidos =nombres+apellidos

archivoNoticias = "40Art.txt"
articulos = cargarcsv(archivoNoticias, "#")

contadorArt=0
nombresPorArticulo = []
for articulo in articulos:
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
        for nombre in nombresApellidos:
            if palabra == nombre:
                esNombre =True
                constructorNombre = constructorNombre+" "+palabra
                nroNombresCostruc = nroNombresCostruc+1
                break
        if not esNombre:
            nombreCompleto=True
        if nombreCompleto:
            if nroNombresCostruc <> 0:
                if nroNombresCostruc > 1:       #no cuenta las entidades aisladas
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
    print articulos[cont-1]
    print cont, nombreArtX, "\n"*2
    cont = cont+1



#quitarle tildes a las palabras. josé no lo reconoce
#problemas con nombres de mas de dos palabras Juan de Dios
#problemas con la base de datos de nombres
    # contiene cosas que no son nombres o apellidos: "Gastos varios"
    # La seccion de apellidos tiene nombres y apellidos en una misma linea
#Implementar: si despues de un nombre la siguiente palabra inicia con mayuscula, es un nombre tambien.

# reconoce organizaciones como apellidos

#Hallazgos:
# los nombres aislados son utiles para encontrar palabras que no estan en la BD de nombres.
# Los alias son facilmente encontrados por las comillas.




