#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
from operator import itemgetter
from AnalisisMorfologico import *
import xlwt

#from operator import itemgetter, attrgetter

def ordenarTablaFrecuencias(palabras, cantidad, valor, columna):
    matriz = []
    for i in range(len(palabras)):
        fila= []
        fila.append(palabras[i])
        fila.append(cantidad[i])
        fila.append(valor[i])
        matriz.append(fila)
    x = sorted(matriz, key=itemgetter(columna))
    return x


articulosCorruptos=["desde", "la"]
s ="Una de las noticias en la recta final de la campaña ha sido su repunte en las últimas encuestas. ¿Qué hizo para dar ese salto? Yo vengo haciendo un trabajo desde hace más de año y medio basado en el contacto permanente con la ciudadanía para saber cuáles con sus problemas y la visión sobre las dificultades de las regiones. Eso me ".split()
a = getIndicesPalabrasClavesOR(s,articulosCorruptos)
print a
exit()


archivoExcel = "clasificacionExpresiones.xls"
expresionesConflictoInterno =  cargarColumnaEnLista(archivoExcel,0,0,1,0)
expresionesMetropolitana = cargarColumnaEnLista(archivoExcel,0,1,1,0)
print expresionesMetropolitana
#expresionesMetropolitana = ["Hola", "nose", "público", "algo"]
exp = "uevo venir a Venezuela a querer dar clase de moral y de libertad policial público ' , señalar"
lista = getOcurrenciasExpresiones(exp,expresionesMetropolitana)
print lista
'''categ, cant =getUniqsConFrecuencias(getOcurrenciasExpresiones(exp,expresionesMetropolitana))
for i in range(len(categ)):
    print categ[i], cant[i]
'''



exit()


style0 = xlwt.easyxf('font: name Times New Roman, colour red, bold on')
wb = xlwt.Workbook()
ws = wb.add_sheet('A Test Sheet',cell_overwrite_ok=True)
ws.write(0, 0, 'Test', style0)
ws.write(2, 0, 4)
ws.write(2, 1, 1)
ws.write(2, 2, xlwt.Formula("A3+B3"))
wb.save('example.xls')


exit()
x= "so i did not for be bad man, i just defend my rights"
patronFin = "just"
indicein = x.find("be")
indiceFin= x.find(patronFin,indicein)
print x[indicein:indiceFin]

hola = [[],[]]

hola[0].append(4)
hola[1].append(5)
print hola[1][0]