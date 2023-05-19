import requests
from bs4 import BeautifulSoup as bs
from markdownify import markdownify as md
import os
import sys
import time


class dataSC(object):
    """Obtiene los datos desde la web y los guarda como Markdown."""

    def __init__(self, url):
        self.url = url
        self.prev = ""
        self.base = 'https://interactivechaos.com'
        self.sopa = ""
        self.index = 2

    def writeIndex(self):
        """Escribe el índice del documento."""

        self.prepare()
        listaLineas = []

        r = requests.get(self.url)
        sopa = bs(r.text, "html.parser")
        s = sopa.find(attrs={'class': 'col-sm-3'})
        menu = s.find(attrs={'class': 'menu'})
        li = menu.find_all('li')

        listaLineas.append(f'# Contenido\n\n')

        i = 1
        for item in li:
            link = item.find("a").get("href").split('/')[-1]
            nameItem = item.text.strip()
            linea = f'{i}. [{nameItem}](#{nameItem.replace(" ", "-").lower()})\n'
            listaLineas.append(linea)
            i += 1

        listaLineas.append('\n\pagebreak')
        with open('mds/01-index.md', 'w') as file:
            file.writelines([i for i in listaLineas])

    def getDataPage(self):
        """Loop, obtiene y guarda la información en un MD por página."""

        self.prepare()

        while self.url != self.prev:
            time.sleep(1)
            #print(self.url)

            r = requests.get(self.url)
            self.sopa = bs(r.text, "html.parser")

            content = self.sopa.find(attrs={'class': 'region region-content'})

            title = content.find('h1', attrs={'class': 'page-title'}).text.strip()

            articulo = content.find('article')
            cuerpo = articulo.find_all('div')[0].find_all('div')[0]

            imagenes = cuerpo.find_all('img')

            codes = cuerpo.find_all('div', {'class', 'codigo'})

            for c in codes:
                br = self.sopa.new_tag('br')
                n = self.sopa.new_tag('code')
                n.string = f'``python\n{c.find("p").text}\n``'
                c.replace_with(n)
                c.append(br)

            for img in imagenes:
                br = self.sopa.new_tag('br')
                urlImage = self.base + img.get('src')
                img['src'] = urlImage
                img.append(br)
                img.append(br)

            markdown = md(f'{cuerpo}')
            enlace = f'<a href="{title.replace(" ","-").lower()}"></a>'
            final = f'{enlace}\n\n# {title}\n\n{markdown}\n\n \pagebreak'

            i = ""
            if self.index < 10:
                i = f'0{self.index}'
            else:
                i = f'{self.index}'

            with open(f'mds/{i}-{title.replace(" ", "_")}.md', 'w') as file:
                file.write(final)

            self.index += 1

            try:
                next = self.sopa.find(
                    attrs={'class': 'book-pager__item book-pager__item--next'}
                    ).find('a').get('href')
                if next is not None:
                    self.prev = self.url
                    self.url = self.base + next.strip()
                    r = requests.get(self.url)
                    self.sopa = bs(r.text, "html.parser")
                else:
                    return ""
            except AttributeError:
                print("Fin")
                sys.exit(1)
                break

    def prepare(self):
        b = os.path.exists('mds')
        if b is not True:
            os.mkdir('mds')
        else:
            print('Existe')


# Datos obtenidos desde la web.
# https://interactivechaos.com/es/course/tutorial-de-pandas
# Créditos a sus creadores.

numpy = 'https://interactivechaos.com/es/manual/tutorial-de-numpy/tutorial-de-numpy'
#base = 'https://interactivechaos.com/es/manual/tutorial-de-pandas/tutorial-de-pandas'

clase = dataSC(base)
clase.writeIndex()
clase.getDataPage()
