#!/usr/bin/python
# -*- coding: utf-8 -*-

import xlwt

from AnalisisLinguistico.AnalisisMorfologico import *


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


mayus = "Palabra"
minus = "palabra"

if mayus[0].isupper():
    print mayus, "is upper"

if mayus[0].islower():
    print mayus, "is lower"

if minus[0].islower():
    print minus, "is lower"


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