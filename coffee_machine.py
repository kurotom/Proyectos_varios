import csv
import os
from time import sleep


def escritura_datos(nombre_fichero, informacion):
    with open(nombre_fichero, "w") as file:
        writer = csv.writer(file, delimiter=",")
        for item in informacion:
            writer.writerow(item)


class MachineCoffee:

    def __init__(self):
        self.agua_consumida = []
        self.leche_consumida = []
        self.chocolate_consumido = []
        self.cafe_consumido = []
        self.azucar_consumida = []
        self.vasos_usados = []

    def print_estado(self):
        consu_file = "consumibles_stats.csv"
        if os.path.exists(consu_file):
            with open(consu_file, "r") as fl_r:
                lector = csv.reader(fl_r, delimiter=",")
                itms = [it for it in lector][1]
            string = f"""\n*** Estado consumibles: ***
        * Agua: \t\t{itms[0]} ml
        * Leche: \t\t{itms[1]} ml
        * Chocolate: \t\t{itms[2]} gr
        * Café: \t\t{itms[3]} gr
        * Azúcar: \t\t{itms[4]} gr
        * Vasos: \t\t{itms[5]} uds
{'*' * 27}\n"""
            return string
        else:
            print("La maquina está vacía, ¿llenar?")
            pregunta = input("1) Si\n2) No\n>>>:  ")
            if pregunta == "1":
                cabezal = "Agua (ml)", "Leche (ml)", "Chocolate (gr)", "Cafe (gr)", "Azucar (gr)", "Vasos (uds)"
                consumibles = [1500, 1000, 500, 300, 100, 10]
                escritura_datos("consumibles_stats.csv", [cabezal, consumibles])
                return "|---  Consumibles Llenos  ---|"
            else:
                return "Se recomienda llenar la máquina."

    def estado_ingrediente(self):
        consu_file = "consumibles_stats.csv"
        if os.path.exists(consu_file):
            with open(consu_file) as file_read:
                reader = csv.reader(file_read)
                niveles_consumibles = [x for x in reader][1]
            agua_resto = float(niveles_consumibles[0]) - sum(self.agua_consumida)
            leche_resto = float(niveles_consumibles[1]) - sum(self.leche_consumida)
            chocolate_resto = float(niveles_consumibles[2]) - sum(self.chocolate_consumido)
            cafe_resto = float(niveles_consumibles[3]) - sum(self.cafe_consumido)
            azucar_resto = float(niveles_consumibles[4]) - sum(self.azucar_consumida)
            vasos_resto = float(niveles_consumibles[5]) - sum(self.vasos_usados)

            if agua_resto <= 0:
                return 1, "Agua insuficiente, depósito vacío."
            elif leche_resto <= 0:
                return 1, "Leche insuficiente, depósito vacío."
            elif chocolate_resto <= 0:
                return 1, "Chocolate insuficiente, depósito vacío."
            elif cafe_resto <= 0:
                return 1, "Cafe insuficiente, depósito vacío."
            elif azucar_resto <= 0:
                return 1, "Azucar insuficiente, depósito vacío."
            elif vasos_resto <= -1:
                return 1, "Vasos insuficiente, depósito vacío."
            else:
                cabezal = "Agua (ml)", "Leche (ml)", "Chocolate (gr)", "Cafe (gr)", "Azucar (gr)", "Vasos (uds)"
                stats = agua_resto, leche_resto, chocolate_resto, cafe_resto, azucar_resto, vasos_resto
                with open(consu_file, "w") as file_write:
                    rows = csv.writer(file_write, delimiter=",")
                    rows.writerow(cabezal)
                    rows.writerow(stats)
                return 0, "Café listo.\n"
        else:
            agua_capacidad = 1500 - sum(self.agua_consumida)  # ml
            leche_capacidad = 1000 - sum(self.leche_consumida)  # ml
            chocolate_capacidad = 500 - sum(self.chocolate_consumido)  # g
            cafe_capacidad = 300 - sum(self.cafe_consumido)  # g
            azucar_capacidad = 100 - sum(self.azucar_consumida)  # g
            vasos_capacidad = 10 - sum(self.vasos_usados)  # unidad

            cabezal = "Agua (ml)", "Leche (ml)", "Chocolate (gr)", "Cafe (gr)", "Azucar (gr)", "Vasos (uds)"
            stats = agua_capacidad, leche_capacidad, chocolate_capacidad, cafe_capacidad, azucar_capacidad, vasos_capacidad
            with open("consumibles_stats.csv", "w") as file_csv:
                escritura = csv.writer(file_csv, delimiter=",")
                escritura.writerow(cabezal)
                escritura.writerow(stats)

    def espresso(self):
        cafe = 7.5
        agua = 30
        vaso = 1
        self.agua_consumida.append(agua)
        self.cafe_consumido.append(cafe)
        self.vasos_usados.append(vaso)
        respuesta = input("¿Azucar?\n 1) Si\n 2) No\n >>>: ")
        if respuesta == "1":
            azucar = 5
            self.azucar_consumida.append(azucar)

    def capuccino(self):
        cafe = 15
        agua = 60
        leche = 60
        leche_espuma = 60
        vaso = 1
        self.agua_consumida.append(agua)
        self.cafe_consumido.append(cafe)
        self.leche_consumida.append(leche + leche_espuma)
        self.vasos_usados.append(vaso)
        respuesta = input("¿Azucar?\n 1) Si\n 2) No\n >>>: ")
        if respuesta == "1":
            azucar = 5
            self.azucar_consumida.append(azucar)

    def late(self):
        cafe = 15
        agua = 60
        leche = 160
        leche_espuma = 10
        vaso = 1
        self.agua_consumida.append(agua)
        self.cafe_consumido.append(cafe)
        self.leche_consumida.append(leche + leche_espuma)
        self.vasos_usados.append(vaso)
        respuesta = input("¿Azucar?\n 1) Si\n 2) No\n >>>: ")
        if respuesta == "1":
            azucar = 5
            self.azucar_consumida.append(azucar)

    def mocha(self):
        cafe = 15
        agua = 120
        leche = 30
        chocolate = 15
        vaso = 1
        self.agua_consumida.append(agua)
        self.cafe_consumido.append(cafe)
        self.leche_consumida.append(leche)
        self.chocolate_consumido.append(chocolate)
        self.vasos_usados.append(vaso)
        respuesta = input("¿Azucar?\n 1) Si\n 2) No\n >>>: ")
        if respuesta == "1":
            azucar = 5
            self.azucar_consumida.append(azucar)


def main():
    while True:
        machine = MachineCoffee()
        print("")
        print("Coffee Machine")
        print("Opciones: \n 1) Comprar\n 2) Estado consumible\n 3) Llenar consumibles\n 4) Salir")
        opt = input("Ingrese opcion: ")
        if opt == "4":
            print("Saliendo...")
            break
        elif opt == "1":
            print("|---------------------------------------------------------------|")
            print("| 1: espresso | 2: capuccino | 3: late | 4: mocha | 5: Cancelar |")
            print("|---------------------------------------------------------------|")
            tipo_cafe = input("Seleccione = ")
            if tipo_cafe == "5":
                continue
            elif tipo_cafe == "1":
                machine.espresso()
                estados = machine.estado_ingrediente()
                if estados == 1:
                    print(estados[1])
                else:
                    print("Preparando el cafe...")
                    sleep(2)
                    print("Café listo")
            elif tipo_cafe == "2":
                machine.capuccino()
                estados = machine.estado_ingrediente()
                if estados == 1:
                    print(estados[1])
                else:
                    print("Preparando el cafe...")
                    sleep(2)
                    print("Café listo")
            elif tipo_cafe == "3":
                machine.late()
                estados = machine.estado_ingrediente()
                if estados == 1:
                    print(estados[1])
                else:
                    print("Preparando el cafe...")
                    sleep(2)
                    print("Café listo")
            elif tipo_cafe == "4":
                machine.mocha()
                estados = machine.estado_ingrediente()
                if estados == 1:
                    print(estados[1])
                else:
                    print("Preparando el cafe...")
                    sleep(2)
                    print("Café listo")
        elif opt == "2":
            print(machine.print_estado())
        elif opt == "3":
            cabezal = "Agua (ml)", "Leche (ml)", "Chocolate (gr)", "Cafe (gr)", "Azucar (gr)", "Vasos (uds)"
            consumibles = [1500, 1000, 500, 300, 100, 10]
            escritura_datos("consumibles_stats.csv", [cabezal, consumibles])
            print("Consumibles llenos.")


if __name__ == '__main__':
    main()
