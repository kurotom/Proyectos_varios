#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Hacer que reciba varios links, los almacene, y los procesa.

import pdfkit
import sys


def proceso(lista):
    print(lista)
    for item in lista:
        listaItem = list(item.items())[0]
        if "?" in item:
            continue
        pdfkit.from_url(listaItem[1], listaItem[0])


lista_tupla = []

print("Usar 'x' Para empezar el proceso obtencion de pdf")

items = {}

while True:

    url = input("URL: ")

    if url == '?':
        print("Ingresar URL y nombre de pdf\nPara salir use: 'x'")
    if url == 'x':
        lista_tupla.append(items)
        break


    nombre_pdf = input("Nombre pdf:  ")

    if nombre_pdf == 'x':
        lista_tupla.append(items)
        break
    if nombre_pdf == "?":
        print("Ingresar URL y nombre de pdf\nPara salir use: 'x'")
    items[nombre_pdf] = url


proceso(lista_tupla)


