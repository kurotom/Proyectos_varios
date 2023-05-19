# -*- coding: utf-8 -*-

from time import sleep
import requests
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

        sleep(1)

        infoResponse = requests.get(self.url)

        s = BeautifulSoup(infoResponse.content, 'html.parser')

        t = s.find('table', 'sismologia')
        tr = t.find_all('tr')

        for item in tr:
            td = item.find_all('td')
            if len(td) > 0:
                id = str(uuid4())
                linkMapa = self.url + td[0].find('a').get('href')
                self.dataDict.update({id: [linkMapa]})

        for element in self.dataDict:
            linkData = self.dataDict[element].pop()

            dataDetailResponse = requests.get(linkData)

            sleep(1)

            s = BeautifulSoup(dataDetailResponse.content, 'html.parser')
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

            urlIMG = linkData[:-4] + 'jpeg'
            infoDetail.append(urlIMG)

            self.resultado.append(infoDetail)


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
