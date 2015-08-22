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

---VERSION - EL TIEMPO
Se deeben tener en cuenta las siguientes consideraciones:
La pagina del tiempo parece vigilar los accesos, cancelando el ingreso de la ip cuando son demasiado frecuentes
A nivel de articulo el tiempo presenta diferentes tipos de codificacion de sus articulos, por ej. desde que usa html ya no imprime tildes
A nivel de articulo el tiempo presenta diferentes patrones de inicio y final a partir aprox de marzo 2014, el cambio es difuso.
A nivel de articulo el patron de inicio y final parece mantenerse desde el inicio del periodico hasta el 2013
'''

#'''# NIVEL LISTAS: OBTENER TODAS LAS URL DE LAS NOTICIAS
topeInicio=297
topePag= 5
print "Se procesarán", topePag, "páginas..."
todasUrls = []
todasPagUrls = []
urlsCorruptas = ["ecbloguer"] # ecbloguer es un blog externo de elcolombiano.com


patronInicio= "                <time"
patronFin="<h3>"
patronInicio2="href=\"http:"
patronFin2="\">"

for i in range(topeInicio,topeInicio+topePag+1):
    print "Leyendo página", i,"..."
    url = "http://www.eltiempo.com/archivo/buscar?q=terrorismo&producto=eltiempo&orden=reciente&pagina="+i.__str__()
    print "listado", url
    usock = urlopen(url)
    data = usock.read()
    usock.close()
    #recorto la seccion donde estan las url
    init = str(data).index(patronInicio)
    data = data[init:init+10000]

    listaE= getOcurrenciasExpresion(data,patronInicio2,patronFin2)
    #obtengo urls limpias
    listaE =getUniqs(listaE)
    for url in listaE:
        inapropiado = getOcurrenciasExpresiones(url,urlsCorruptas)
        if inapropiado <> []:
            print "--DESCARTADO-- Se encontro:", inapropiado
            continue
        url = url[len(patronInicio2):len(patronFin2)*-1]
        url= "http:"+url
        todasUrls.append(url)
        todasPagUrls.append(i)
        #print url, "\n"*2

#exit()
# NIVEL DE ARTICULO: OBTENER EL PARRAFO DE LA NOTICIA DEL ARTICULO

nombreArchivoUrls = str(topePag)+"Url.txt"
outputUrl=open(nombreArchivoUrls,"w")
outputUrl.close()   # Reinicio txt
outputUrl = open(nombreArchivoUrls,"a")

nombreArchivo = str(topePag)+"Art.txt"
outputArt=open(nombreArchivo,"w")
outputArt.close()   # Reinicio txt
outputArt = open(nombreArchivo,"a")

#articulosCorruptos=["@"] #tiene hiperlinks de twiter o errores en el patron
articulosCorruptos=[] #tiene hiperlinks de twiter o errores en el patron
patronIn = "<p itemprop='articleBody'>"
patronFin = '<footer class="footer-article">'
patronIn2 = '<div class="columna_articulo">'
patronFin2 = '<div class="compartirTop">'
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
    #print "ARTICULO INICIAL", articulo

    #DESCARTE DE ARTICULOS
    # Si el primer patron falla intento con el segundo
    if len(articulo)<2:
        indiceIn=data.find(patronIn2)
        indiceFin= data.find(patronFin2)
        articulo=data[indiceIn:indiceFin]
        if len(articulo)<2:
            print "--DESCARTADO-- No se encontro el articulo"
            continue
    inapropiado = getOcurrenciasExpresiones(articulo,articulosCorruptos)
    if inapropiado <> []:
        print "--DESCARTADO-- Se encontraron caracteres inapropiados:", inapropiado
        continue

    # limpio (whiteSpaces y simbolos) y almaceno el articulo
    articulo = articulo.replace("\n"," ")
    articulo = deleteExpresion(articulo,"<!--","-->")
    articulo = deleteExpresion(articulo,"<",">")
    articulo = articulo.replace("”"," ' ")
    articulo = articulo.replace("“"," ' ")
    articulo = articulo.replace("‘"," ' ")
    articulo = articulo.replace("’"," ' ")
    articulo = articulo.replace("’"," ' ")
    articulo = articulo.replace('"'," ' ")

    articulo = articulo.replace("—","")
    articulo = articulo.replace("#","")
    #limpio codificacion html
    articulo = articulo.replace("&aacute;","á")
    articulo = articulo.replace("&eacute;","é")
    articulo = articulo.replace("&iacute;","í")
    articulo = articulo.replace("&oacute;","ó")
    articulo = articulo.replace("&uacute;","ú")
    articulo = articulo.replace("&ntilde;","ñ")
    articulo = articulo.replace("&uuml;","ü")
    articulo = articulo.replace("&Aacute;","Á")
    articulo = articulo.replace("&Eacute;","É")
    articulo = articulo.replace("&Iacute;","Í")
    articulo = articulo.replace("&Oacute;","Ó")
    articulo = articulo.replace("&Uacute;","Ú")
    articulo = articulo.replace("&Ntilde;","Ñ")
    articulo = articulo.replace("&Uuml;","Ü")
    articulo = articulo.replace("&iquest;","¿")
    articulo = articulo.replace("&nbsp;"," ")
    articulo = articulo.replace("&ldquo;"," ' ")
    articulo = articulo.replace("&rdquo;"," ' ")
    articulo = articulo.replace("&lsquo;"," ' ")
    articulo = articulo.replace("&rsquo;"," ' ")
    articulo = articulo.replace("&iexcl;"," ¡ ")
    articulo = articulo.replace("&deg;"," ° ")
    articulo = articulo.replace("&ndash;"," - ")
    articulo = articulo.replace("&ordf;"," ")


    articulo = articulo.replace(chr(9),"")      # tabulador normal
    articulo = articulo.replace(chr(10),"")     # tabulador extraño
    articulo = articulo.replace(chr(13),"")     # tabulador extraño 2
    articulo = articulo.strip()

    print "final limpio", articulo


    outputArt.write(articulo+" # ")
    if cantidadArt <>0: #primera iteracion
        outputUrl.write(",")
    outputUrl.write(url)
    cantidadArt+=1
outputArt.close()
outputUrl.close()
print "\nRESULTADO: ",cantidadArt, "articulos salvados en","'"+nombreArchivo+"'", "\nLas urls las puedes encontrar en","'"+nombreArchivoUrls+"'"
# FIN  NIVEL ARTICULO

#se hizo optimizacion de tiempos
# salidas en archivos de compatibilidad
# informe de procesos realizados por consola