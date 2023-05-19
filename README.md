# sismologia_scraping
Datos obtenidos de [http://www.sismologia.cl/](http://www.sismologia.cl/), se puede guardar los datos en un fichero `.csv`.

Utiliza driver [geckodriver - 0.31.0](https://github.com/mozilla/geckodriver/releases).


## Requisitos
* requests==2.27.1
* beautifulsoup4==4.11.0


## ¿Cómo utilizar?

1. Clonar este proyecto.

2. Instalar paquetes.
```
$ pip install -r requirements.txt
```

3. Utilizar el programa.
```
$ python sismologia_scraping.py
```


Formato del fichero '.csv': `sismologia-[timestamp].csv`.

Dicho 'timestamp' es del momento de la consulta de los datos.
