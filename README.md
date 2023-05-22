# Auto_update_mods

Actualiza los 'mods' de una lista a la versión especificada.

Busca, descarga, guarda y comprueba integridad, los almacena en un directorio/carpeta `mods`.

>
> Importante:  construido para la **Versión Java**, busca mods **Forge**.
>

## Requisitos

* Instalar Python

* Instalar dependencias

  ```bash
  pip install -r requirements.txt
  ```

* Una *API key* de [CurseForge - enlace](https://console.curseforge.com/#/login)
  - Se debe crear una cuenta y obtener la *api key*
  - La llave obtenida se debe guardar en un archivo de texto (`.txt`) para poder acceder posteriormente.

## Modo de uso

Ejecutar en una terminal, la llave debe estar entre comillas simples.

```bash
python update_mods_cli.py [-h] [-f FILENAME] [-m MOD] [-g GAMEVERSION] [-k 'apiKey']
```

| Opciones | Descripción |
|-|-|
| -h, --help | Muestra ayuda. |
| -f FILENAME, --filename FILENAME | fichero de texto (`.txt`) con lista de todos los mods. |
| -m MOD, --mod MOD | nombre del fichero del mod para actualizar. |
| -g GAMEVERSION, --gameVersion GAMEVERSION | versión del juego. |
| -k 'apiKey', --key 'apiKey' | API key, entre comillas simples (`' '`). |

Para consultar la versión del juego ir a la [Java Edition version history](https://minecraft.fandom.com/wiki/Java_Edition_version_history)
