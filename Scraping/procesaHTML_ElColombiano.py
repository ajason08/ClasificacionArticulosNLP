#!/usr/bin/python
# -*- coding: utf-8 -*-

from urllib import *
import re
from AnalisisMorfologico import *
import timeit

'''
ini = timeit.timeit()
fin = timeit.timeit()
print abs((fin-ini)*1000)
'''

'''
ESTE SCRIPT OBTENDRÁ TODAS LOS ARTICULOS DE UNA PAGINA WEB DE PERIODICOS LA CUAL CUMPLA CON PATRONES DE SCRABING,
SE MUESTRA UN EJEMPLO CON LA PAGINA WEB EL_COLOMBIANO_.COM.
SOLO ES NECESARIO ESPECIFICAR LA URL Y EL TOPE (PAGINA MAX A LA QUE SE DESEA LLEGAR)
'''

#'''# NIVEL LISTAS: OBTENER TODAS LAS URL DE LAS NOTICIAS
topePag= 3

todasUrls = []
todasPagUrls = []
patronInicio= "</span> </div> <figure class=\"img-noticia\"> <a href=\""
patronFin=">"
tampin= len(patronInicio)
urlsCorruptas = ["ecbloguer"] # ecbloguer es un blog externo de elcolombiano.com

print "Se procesarán", topePag, "páginas..."
for i in range(1,topePag+1):
    print "Leyendo página", i,"..."
    url = "http://www.elcolombiano.com/busqueda/-/search/violencia/false/false/19150717/20150717/date/true/true/0/0/meta/0/0/0/"+i.__str__()
    usock = urlopen(url)
    data = usock.read()
    usock.close()
    #recorto la seccion donde estan las url
    init = str(data).index(patronInicio)
    data = data[init:init+10000]
    listaE= getOcurrenciasExpresion(data,patronInicio,patronFin)
    #obtengo las url
    for url in listaE:
        inapropiado = getOcurrenciasExpresiones(url,urlsCorruptas)
        if inapropiado <> []:
            continue
        url=url[tampin:-2]
        url= "http://www.elcolombiano.com"+url
        todasUrls.append(url)
        todasPagUrls.append(i)


#''' # NIVEL DE ARTICULO: OBTENER EL PARRAFO DE LA NOTICIA DEL ARTICULO

nombreArchivoUrls = str(topePag)+"Url.txt"
outputUrl=open(nombreArchivoUrls,"w")
outputUrl.close()   # Reinicio txt
outputUrl = open(nombreArchivoUrls,"a")

nombreArchivo = str(topePag)+"Art.txt"
outputArt=open(nombreArchivo,"w")
outputArt.close()
outputArt = open(nombreArchivo,"a")

articulosCorruptos=["@","&nbsp"] #tiene hiperlinks de twiter o errores en el patron
patronIn = "<!-- cxenseparse_start -->"
patronFin = "</p> </div> </article>"
j=1
cantidadArt=0
for url in todasUrls:
    #obtengo articulo
    usock = urlopen(url)
    data = usock.read()
    usock.close()
    indiceIn=data.find(patronIn)
    indiceFin= data.find(patronFin)
    articulo=data[indiceIn:indiceFin]

    #determino si el articulo es valido
    print "--------ARTICULO NUEVO ----------", j, "pagina", todasPagUrls[j-1]
    print url
    j=j+1
    x = getOcurrenciasExpresiones(articulo,articulosCorruptos)
    if x <> []:
        print "--DESCARTADO--"
        continue

    # limpio (whiteSpaces y simbolos) y almaceno el articulo
    articulo = re.sub('[\t]+' , ' ', articulo).strip()
    articulo = deleteExpresion(articulo,"<",">")
    articulo = articulo.replace("”"," ' ")
    articulo = articulo.replace("“"," ' ")
    articulo = articulo.replace("‘"," ' ")
    articulo = articulo.replace("’"," ' ")
    articulo = articulo.replace("’"," ' ")
    articulo = articulo.replace("—","")
    articulo = articulo.replace("#","")
    print articulo


    outputArt.write(articulo+" # ")
    if cantidadArt <>0: #primera iteracion
        outputUrl.write(",")
    outputUrl.write(url)
    cantidadArt+=1
outputArt.close()
outputUrl.close()
print "\n ",cantidadArt, "articulos salvados en","'"+nombreArchivo+"'", "\nLas urls las puedes encontrar en","'"+nombreArchivoUrls+"'"
#''' # FIN  NIVEL ARTICULO

#se hizo optimizacion de tiempos
# salidas en archivos de compatibilidad
# informe de procesos realizados por consola