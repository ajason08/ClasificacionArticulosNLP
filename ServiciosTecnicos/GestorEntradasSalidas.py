#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import xlrd
import xlwt
import prettytable
from operator import itemgetter


def cargarArchivoTaggerTNT(archivo):
    palabras = []
    categorias = []
    lemas = []
    with open(archivo, 'r') as f:
        myString = f.read()    # con el decode(latin-1) reemplaza 'í' i tildada por 'Ã­'
    b= myString.split('\n')
    i=0

    if b[-1].split('\t')==['']: # se elimina si al final no saco la ultima linea completa
        b=b[0:-1]

    for x in b:
        t=1
        bb= x.split('\t')
        if len(bb)<>3:
            print "aqui esta", bb
        for xx in bb:
         #   print "celda", xx, i
            if i%3==0:
                palabras.append(xx)
            elif i%3==1:
                categorias.append(xx)
            elif i%3==2:
                lemas.append(xx)                                     # al imprimir cada una la saca bien, centímetros
            i=i+1

    return palabras, categorias, lemas




def cargarcsv(archivo, signoSeparacion=","):
    with open(archivo, 'r') as f:
        myString = f.read()    # con el decode(latin-1) reemplaza 'í' i tildada por 'Ã­'
    b= myString.split(signoSeparacion)
    return  b

def exportarExcelClasificacion(urls, clasificacion, nombre="outputClasificacion.xls"):
    style0 = xlwt.easyxf('font: name Times New Roman, colour red, bold on')
    wb = xlwt.Workbook()
    ws = wb.add_sheet('A Test Sheet',cell_overwrite_ok=True)
    ws.write(0, 0, 'LINK', style0)
    ws.write(0, 1, 'CLASIFICACION', style0)
    for i in range (len(urls)):
        #ws.write(i+1, 0, articulos[i])
        ws.write(i+1, 0, urls[i])
        ws.write(i+1, 1, clasificacion[i])
    wb.save(nombre)
    print "Archivo exportado como", nombre

def cargarLematizacion2(archivo):
    tagger = []
    with open(archivo, 'r') as f:
        myString = f.read()    # con el decode(latin-1) reemplaza 'í' i tildada por 'Ã­'
    b= myString.split('\n')
    i=0
    for x in b:
        bb= x.split('\t')
        tagger.append(bb)
    return tagger

def ordenarTabla(columnas,c):
    #ordena una matriz procedente de vectores de la forma [vector0, vector1, vectorn],
    #c es el numero del vector por el cual se ordenara la matriz
    if not c in range(len(columnas)):
        print "Excepcion c is not in range of matrix"
        return None
    nroFilas=len(columnas[0])
    matriz = []
    for i in range(nroFilas):
        fila= []
        for columna in columnas:
            fila.append(columna[i])
        matriz.append(fila)
    x = sorted(matriz, key=itemgetter(c))
    return x

def cargarColumnaEnLista(excel, hoja, columna, filainicial=0, filaLimite=0):
    # dado un archivo excel, una hoja y una columna(inicia en 0) se cargaran los datos en una
    # hasta llegar a una celda vacia o hasta la fila limite establecida
    doc = xlrd.open_workbook(excel)
    sheet = doc.sheet_by_index(hoja)
    if filaLimite == 0:
        nrows = sheet.nrows
        filaLimite = nrows
    lista = []
    a = ""
    for i in range(filainicial, filaLimite+1):
        try:
            celda = sheet.cell_value(i,columna).__str__()
            if celda == '':                                   # una celda vacia indica que la columna no tiene mas valores
                break
            lista.append(celda.encode())
        except:
            celda= sheet.cell_value(i, columna)
            #print celda, "execepcion!!", sys.exc_info()[0]
            #continue
            if celda=='':                                   # una celda vacia indica que la columna no tiene mas valores
                break
            lista.append(celda.encode('utf-8'))# el encode lo agregue para que no saque las palabras tildadas como unicode
    return lista
