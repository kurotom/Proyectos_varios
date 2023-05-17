# Incorporar ruta para guardar mods
#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import re
import threading
from decouple import config

from clase.AutoUpdateClass import AutoUpdate


def main():
    parser = argparse.ArgumentParser(
                        prog='update_mods_cli.py',
                        description='Actualiza mods a la versión especificada.',
                        epilog='Ayuda en el proceso tedioso de actualizar varios mods.'
                    )
    parser.add_argument(
            '-f',
            '--filename',
            type=str,
            help='txt con lista de todos los mods',
        )
    parser.add_argument(
            '-m',
            '--mod',
            type=str,
            help='nombre del fichero del mod'
        )
    parser.add_argument(
            '-g',
            '--gameVersion',
            type=str,
            help='versión del juego'
        )

    args = parser.parse_args()

    filename = args.filename
    mod = args.mod
    gameVersion = args.gameVersion

    if filename is not None or mod is not None and gameVersion is not None:
        reg = re.search(r'^1\.([0-9]{,2}.+)?', gameVersion)
        if reg is None:
            print()
            print("Ingrese una versión correcta")
            print("https://minecraft.fandom.com/wiki/Java_Edition_version_history")
            print()
        else:
            apiKey = config('key_api', cast=str)
            if filename is not None:
                auto = AutoUpdate(key=apiKey, version=gameVersion)
                auto.load_txt(filename)
                tr1 = threading.Thread(target=auto.download)
                tr1.start()
            elif mod is not None:
                auto = AutoUpdate(key=apiKey, version=gameVersion)
                auto.search(mod)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
