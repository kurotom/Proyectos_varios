import requests
import hashlib
import os
from datetime import datetime
import re
from time import sleep


class AutoUpdate(object):

    url = 'https://api.curseforge.com'

    def __init__(self, key=None, version=None):
        """
        Constructor AutoUpdate
        """
        self.mods_update = []

        self.key = key
        self.version = version
        self.current_mod = ""
        self.resultados = []

        self.mod_encontrados = []
        self.no_encontrados = []
        self.error_mod = []

        self.cantidad_encontrado = 0
        self.continueSearch = False
        self.iteraciones_paginas = 0
        self.indice = 0

    def checkKey(self, key):
        """
        Verifica la existencia y el tamaño de la llave API.
        """
        if key != "" and len(key) == 60:
            return True
        else:
            return False

    def setKeyApi(self, key_api=""):
        """
        Establece la llave de API.
        """
        if self.checkKey(key_api):
            self.key = key_api
        else:
            raise ValueError('Key is empty or no longer length.')

    def headers(self):
        """
        Retorna header de la petición.
        """
        if self.key is not None:
            headers = {
                'single': {
                    'Accept': 'application/json',
                    'x-api-key': self.key
                    },
                'multiple': {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'x-api-key': self.key
                    }
                }
            return headers
        else:
            raise ValueError('Api Key not set.')
            return None

    def load_txt(self, path_file_txt):
        """
        Carga el fichero TXT y busca por cada línea.
        """
        try:
            file_txt = os.path.abspath(path_file_txt)
            with open(file_txt, 'r') as file:
                for filename in file.readlines():
                    reg = re.findall(
                        r'([a-zA-Z]+)(?!=forge|Forge|FORGE|jar$)',
                        filename.strip()
                    )
                    if reg:
                        reg.pop(reg.index('jar'))
                        if 'Forge' in reg:
                            reg.pop(reg.index('Forge'))
                        if 'FORGE' in reg:
                            reg.pop(reg.index('FORGE'))
                        if 'forge' in reg:
                            reg.pop(reg.index('forge'))
                        if 'v' in reg:
                            reg.pop(reg.index('v'))
                        if 'mc' in reg:
                            reg.pop(reg.index('mc'))
                        if 'universal' in reg:
                            reg.pop(reg.index('universal'))

                        if len(reg) == 1:
                            self.current_mod = re.sub(
                                    r'(?=[A-Z])', ' ', reg[0]
                                ).strip()
                        else:
                            self.current_mod = " ".join(map(str, reg))

                        sleep(1)

                        ltiempo = f'{self.tiempo()}'
                        lbody = '  Searching     ---  '
                        lcurrent = f'{self.current_mod}'
                        print(ltiempo + lbody + lcurrent)

                        self.search(
                                self.current_mod,
                                filename
                            )
        except KeyboardInterrupt:
            print('\nInterrumpido por el usuario')

    def search(self, mod_string=None, fileModOrigin=None, indice=0):
        """
        Busca por nombre del mod.
        """
        if self.key is None:
            raise ValueError('Key API no establecida.')
        else:
            if mod_string is not None:
                self.current_mod = mod_string.strip()

            parametros = {
                'gameId': 432,
                # 'gameVersion': '1.19.2',
                'gameVersion': self.version,
                'searchFilter': self.current_mod.lower(),
                'modLoader': 1,
                'modLoaderType': 1,
                'sortField': 8,
                'sortOrder': 'asc'
            }

            url = self.url + '/v1/mods/search' + f'?index={indice}'
            res = requests.get(
                url=url,
                headers=self.headers()['single'],
                params=parametros
            )

            resJSON = res.json()

            self.resultados = resJSON['data']

            if len(self.resultados) == 0:
                print("No encontrado\n")
                if fileModOrigin not in self.no_encontrados:
                    self.no_encontrados.append(fileModOrigin)
            if len(self.resultados) > 0:
                if fileModOrigin is not None:
                    # print('1----')
                    self.filtrarResultados(
                        self.current_mod,
                        fileModOrigin
                    )
                else:
                    # print('2----')
                    self.filtrarResultados(
                        self.current_mod
                    )

                # totalPaginas = 4
                # itemPaginas = self.indice
                totalPaginas = resJSON["pagination"]["totalCount"] + 1
                itemPaginas = resJSON["pagination"]["index"]
                # print(f'Continua buscando?:  {self.continueSearch}')
                #
                # print(
                #         itemPaginas,
                #         totalPaginas,
                #         self.continueSearch
                #     )
                # print()

                if itemPaginas < totalPaginas and self.continueSearch:
                    indice += 1
                    self.search(mod_string, fileModOrigin, indice)

    def comparar(self, modEncontrado, original):
        """
        Compara el nombre del fichero actual con el encontrado.
        """
        # print('comparando    ---', modEncontrado, original)
        boleano = [
                self.current_mod.replace(" ", "") in modEncontrado,
                self.current_mod.replace(" ", "-") in modEncontrado,
                self.current_mod.replace(" ", "_") in modEncontrado
            ]

        if any(boleano):
            i = 1
            for x in range(len(modEncontrado)):
                if modEncontrado[x] == original[x]:
                    # print(a[x], b[x], a[x] == b[x], i)
                    i += 1
                else:
                    break
            resultado = {"score": i, "item": modEncontrado}
            return resultado
        else:
            return None

    def filtrarResultados(self, modString, modFileOrigin=None):
        """
        Filtra resultados de los mods encontrados.
        """
        # print(f'filteredFile  ---  {modString} | {modFileOrigin}')

        resultado_filtrados = []
        fichero_retorno = {}

        for item in self.resultados:
            for it in item['latestFilesIndexes']:
                resultado = self.comparar(it['filename'], modFileOrigin)
                if resultado is not None:
                    resultado['slug'] = item['slug']
                    resultado['modId'] = item['id']
                    resultado['name'] = item['name']
                    resultado_filtrados.append(resultado)

        if len(resultado_filtrados) > 0:
            x = max([i['score'] for i in resultado_filtrados])
            y = [i for i in resultado_filtrados if i['score'] == x]
            # print(y, len(y))

            # Busca en resultado filtrando por slug en base al
            # fichero con score mayor retornado de 'self.comparar'
            lista_mods = [
                    item for item in self.resultados
                    if item['slug'] == y[0]['slug']
                ]

            for item in lista_mods:
                fileIndex = [
                        i for i in item['latestFilesIndexes']
                        if i['gameVersion'] == '1.19.2'
                        if 'modLoader' in i.keys()
                        if i['modLoader'] == 1
                    ][0]
                # print()
                # print(fileIndex)
                # print()
                fileIndex['modId'] = item['id']
                fileIndex['name'] = item['name']
                fileIndex['slug'] = item['slug']
                fichero_retorno = fileIndex

            if fichero_retorno not in self.mod_encontrados:
                print("Encontrado")
                self.mod_encontrados.append(fichero_retorno)

            self.cantidad_encontrado += 1
            self.continueSearch = False
            return fichero_retorno
        else:
            self.continueSearch = True
            return None

    def download(self):
        """
        Descarga y guarda el fichero del mod
        """
        if self.key != "":
            if len(self.mod_encontrados) == 0:
                print("Lista de mods encontrados está Vacía.")
            elif len(self.mod_encontrados) > 0:
                print(f'{self.tiempo()}  Descargando mod')
                for item in self.mod_encontrados:
                    try:
                        itemID = f'/v1/mods/{item["modId"]}'
                        fileID = f'/files/{item["fileId"]}'
                        url = self.url + itemID + fileID

                        res = requests.get(
                                url,
                                headers=self.headers()['single']
                            )

                        data = res.json()['data']

                        hashSha1 = data['hashes'][0]['value']
                        filename = data['fileName']
                        fileUrl = data['downloadUrl']

                        requestMod = requests.get(
                                fileUrl,
                                headers=self.headers()['single']
                            )
                        # print(requestMod.status_code)
                        ruta = self.save(
                                filename,
                                requestMod.content
                            )
                        self.check_integrity(ruta, hashSha1)
                    except Exception:
                        print('Error mod', item)
                        elemento = item['filename'], item['modId']
                        self.error_mod.append(elemento)
                else:
                    if len(self.mod_encontrados) > 1:
                        print(f"\n{self.tiempo()}  Mods descargados en 'mods'")
                    else:
                        print(f"\n{self.tiempo()}  Mod descargado en 'mods'")
            self.writeLog()
        else:
            raise ValueError('LLave API no establecida.')

    def save(self, filename, content):
        """
        Guarda el mod encontrado en la carpeta 'mods'
        """
        print("___>")
        existe = os.path.exists('mods')
        if not existe:
            os.mkdir('mods')

        path = f'mods/{filename}'

        with open(path, 'wb') as file:
            file.write(content)
        return path

    def check_integrity(self, mod, sha1, md5=None):
        """
        Comprueba la integridad del fichero usando sha1 (default) y/o md5.
        """
        pathMod = os.path.abspath(mod)
        name = mod.split("/")[-1]
        hash = ""
        # print(pathMod)
        with open(pathMod, 'rb') as fl:
            hash = hashlib.sha1(fl.read()).hexdigest()
        if sha1 != hash:
            print(f'{name} -> Mod con error')
            file = {
                    "name": name,
                    "sha1": hash,
                    "date": str(datetime.now())
                }
            self.error_mod.append(file)
        else:
            print(f'{name} -> Mod correcto')

    def writeLog(self):
        """
        Escribe LOGs de los mods encontrados y los no.
        """
        # print(self.no_encontrados)
        econtrados = [f'{i["filename"]}\n' for i in self.mod_encontrados]
        no_econtrados = [f'{i}\n' for i in self.no_encontrados]
        with open("mods_actualizados.log", "w") as file:
            file.writelines(econtrados)

        with open("no_encontrados.log", "w") as file:
            file.writelines(no_econtrados)

        if len(self.error_mod) > 0:
            lineas = [f'{i}\n' for i in self.error_mod]
            with open("error_mods.log", "w") as file:
                file.writelines(lineas)

    def __str__(self):
        """
        Imprime los mods encontrados y la cantidad.
        """
        l1 = f'{self.mod_encontrados}'
        l2 = '\nEncontrados: {self.cantidad_encontrado}'
        return l1 + l2

    def showError(self):
        """
        Imprime los mods que presentaron errores al buscar.
        """
        print("\n".join(map(str, self.error_mod)))

    def tiempo(self):
        """
        Retorna el tiempo actual en formato '%H:%M:%S - %d/%m/%Y'
        """
        return datetime.strftime(datetime.now(), '%H:%M:%S - %d/%m/%Y')
