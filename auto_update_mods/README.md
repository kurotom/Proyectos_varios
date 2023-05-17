# Auto_update_mods

Actualiza los 'mods' de una lista a la versión especificada.

Busca, descarga, guarda y comprueba integridad, los almacena en un directorio/carpeta `mods`.

>
> Importante:  construido para la **Versión Java**.
>

## Requisitos

* Instalar Python

* Instalar dependencias

  ```bash
  pip install -r requirements.txt
  ```

* Una *API key* de [CurseForge - enlace](https://console.curseforge.com/#/login)
  - Se debe crear una cuenta y obtener la *api key*
  - Debe ser guardada en el directorio principal del programa, dentro de un fichero `.env`, la llave debe estar entre comillas, con el siguiente formato:
  ```
  key_api='api_key_curse_forge'
  ```
  - El programa leerá directamente `.env` buscando la llave.


## Modo de uso

Ejecutar en una terminal.

```bash
python update_mods_cli.py [-h] [-f FILENAME] [-m MOD] [-g GAMEVERSION]
```

| Opciones | Descripción |
|-|-|
| -h, --help | Muestra ayuda. |
| -f FILENAME, --filename FILENAME | fichero de texto (`.txt`) con lista de todos los mods. |
| -m MOD, --mod MOD | nombre del fichero del mod para actualizar. |
| -g GAMEVERSION, --gameVersion GAMEVERSION | versión del juego. |

Para consultar la versión del juego ir a la [Java Edition version history](https://minecraft.fandom.com/wiki/Java_Edition_version_history)
