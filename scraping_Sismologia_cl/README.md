# sismologia_scraping
Datos obtenidos de [http://www.sismologia.cl/](http://www.sismologia.cl/), se puede guardar los datos en un ficheros `.csv`.

Utiliza driver [geckodriver - 0.31.0](https://github.com/mozilla/geckodriver/releases).


## Requisitos
* selenium==4.1.3
* beautifulsoup4==4.11.0


## ¿Cómo utilizar?

```
$ pip install -r requirements.txt
```

```
$ python sismologia_scraping.py
```


Los datos se guardarán en un fichero '.csv' en el formato: `sismologia-[timestamp].csv`.
Dicho 'timestamp' es del momento de la realización de la consulta de los datos.
