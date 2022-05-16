# -*- coding: utf-8 -*-
from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import json

url = "http://www.sismologia.cl"

opciones = Options()
opciones.headless = True

driver = webdriver.Firefox(options=opciones, executable_path="geckodriver/geckodriver")
driver.get(url)

sleep(3)

frameset = driver.find_element_by_xpath("/html/frameset/frame[2]")
driver.switch_to.frame(frameset)
fr2 = driver.find_element_by_xpath("/html/frameset/frame[2]")
driver.switch_to.frame(fr2)

fr3 = driver.find_element_by_xpath("/html/body/div/div/div[2]/iframe")
driver.switch_to.frame(fr3)

tabla_datos = driver.find_elements_by_xpath("/html/body/table/tbody")

lista = []
for x in tabla_datos:
    lista = x.text.split("\n")

driver.close()


fin = []
i = 0
for x in lista:
    if len(x.split()) > 4:
        fecha = x.split()[:2]
        ubicacion = x.split()[2:len(x.split()) - 2]
        magnitud = x.split()[len(x.split()) - 2:]
        res = {"fecha": " ".join(fecha), "ubicacion": " ".join(ubicacion), "magnitud": " ".join(magnitud)}
        fin.append(res)
    i += 1

with open("temblores.json", "w") as file:
    json.dump(fin, file)
