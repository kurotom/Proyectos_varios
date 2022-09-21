# -*- coding: utf-8 -*-
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

from bs4 import BeautifulSoup
from uuid import uuid4
import datetime
import json
import os
import csv


class SismologiaData(object):
    def __init__(self, url, path):
        self.url = url
        self.agente = path
        self.dataDict = {}
        self.resultado = []
        self.date = 0

    def run(self):
        self.date = int(datetime.datetime.now().timestamp())

        opciones = Options()
        opciones.headless = True

        serviceObject = Service(self.agente)

        driver = webdriver.Firefox(options=opciones, service=serviceObject)
        driver.get(self.url)

        sleep(3)

        page = driver.page_source

        s = BeautifulSoup(page, 'html.parser')

        t = s.find('table', 'sismologia')
        tr = t.find_all('tr')

        for item in tr:
            td = item.find_all('td')
            if len(td) > 0:
                id = str(uuid4())
                linkMapa = self.url + td[0].find('a').get('href')
                self.dataDict.update({id: [linkMapa]})

        for element in self.dataDict:
            info = self.dataDict[element].pop()

            driver.get(info)

            sleep(3)

            s = BeautifulSoup(driver.page_source, 'html.parser')
            tabla = s.find('table', "sismologia informe")
            trs = tabla.find_all('tr')

            infoDetail = []
            for l in range(len(trs)):
                if l == 1 or l == 2:
                    td = trs[l].find_all('td')
                    fechaHora = td[1].text.split()
                    for dItem in fechaHora:
                        infoDetail.append(dItem)
                else:
                    td = trs[l].find_all('td')
                    infoDetail.append(td[1].text.strip())

            urlIMG = info[:-4] + 'jpeg'
            infoDetail.append(urlIMG)

            self.resultado.append(infoDetail)

        driver.close()

    def write(self):
        keysData = [
            'Referencia',
            'Hora local',
            'Fecha local',
            'Hora UTC',
            'Fecha UTC',
            'Latitud',
            'Longitud',
            'Profundidad',
            'Magnitud',
            'Mapa'
        ]
        with open(f'sismologia-{self.date}.csv', 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(keysData)
            for line in self.resultado:
                writer.writerow(line)




if __name__ == '__main__':
    url = "http://www.sismologia.cl"
    path = os.path.abspath("geckodriver")
    s = SismologiaData(url, path)
    s.run()
    s.write()
