import random
import string


# Parametro Faltante: >>> nivel <<<
def cortar_palabra(palabra_usada):
    rango = 0
    res = []
    plbr = palabra_usada.lower()
    # facil
    if len(plbr) <= 4:
        rango = 1
    # medio
    elif 4 < len(plbr) < 10:
        rango = 3
    # dificil
    elif 10 <= len(plbr) < 20:
        rango = 5
    # imposible
    elif len(plbr) >= 20:
        rango = 10

    for x in range(rango + 1):
        if not res:
            res.append(palabra.replace(palabra[random.randint(0, len(palabra) - 1)], " "))
        else:
            string_afiltrar = res[0]
            res.clear()
            res.append(string_afiltrar.replace(palabra[random.randint(0, len(palabra) - 1)], " "))
    return res[0].replace(" ", "_")


def orden_ubicacion_letras(resultado_palabra_cortada, palabra_completa):
    letras_unicas = []
    todas_letras_faltantes = []
    for t in range(len(resultado_palabra_cortada)):
        if resultado_palabra_cortada[t] == "_":
            ubicacion_palabra = palabra_completa[t], t
            todas_letras_faltantes.append(ubicacion_palabra)
            if palabra_completa[t] not in letras_unicas:
                letras_unicas.append(palabra[t])
    i = 0
    lista_items = []
    for _ in range(len(letras_unicas)):
        repeticiones = []
        for faltante_tupla in todas_letras_faltantes:
            if faltante_tupla[0] == letras_unicas[i]:
                repeticiones.append(faltante_tupla[1])
        item = {letras_unicas[i]: repeticiones}
        lista_items.append(item)
        i += 1
    return lista_items


def main_del_juego(palabra_incognita):
    key = []
    orden_letras = orden_ubicacion_letras(palabra_incognita, palabra)
    for x in orden_letras:
        key.append(list(x.keys())[0])

    # bolsa de mezclado de letras
    letas_distraccion = []
    i = 0
    while i < ((len(key) * 2) + 1):
        for k in key:
            letra_gen = string.ascii_lowercase[random.randrange(0, len(string.ascii_lowercase))]
            if letra_gen != k:
                letas_distraccion.append(letra_gen)
                i += 1
    for itm in key:
        letas_distraccion.insert(random.randrange(0, len(letas_distraccion)), itm)

    posicion_index = []
    for xx in orden_letras:
        for i in list(xx.values()):
            for t in range(len(i)):
                posicion_index.append(i[t])
    posicion_index.sort()

    return posicion_index, letas_distraccion


def reemplazo_letras(posicion_cambio, letter_usada, palabra_cut):
    pal = f"{palabra_cut[:posicion_cambio]}" + f"{letter_usada}" + f"{palabra_cut[posicion_cambio + 1:]}"
    return pal


def print_ahorcado(ojos, boca):
    string_ahorcado = f"""
       ------------------
       |                |
       |                |
       |             ________
       |            | {ojos} {ojos}  |
       |       \    | {boca}  |   /
       |        \   |________|  /
       |         \      ||     /
       |           \----||----/
       |                ||
       |                ||
       |                ||
       |               |  |
       |              |    |
       |              |    |
     ./|\.
    --------------------------------
    --------------------------------
    """
    return string_ahorcado


def print_win(ojos, boca):
    string_ahorcado = f"""
       ------------------
       |                |
       |                
       |
       |             ________
       |            | {ojos} {ojos}  |
       |       \    | {boca}  |   /
       |        \   |________|  /
       |         \      ||     /
       |           \----||----/
       |                ||
       |                ||
       |                ||
       |               |  |
       |              |    |
     ./|\.            |    |
    --------------------------------
    --------------------------------
    """
    return string_ahorcado

#
#
#
#  Inicio del programa


file_words = "words.txt"
with open(file_words, "r") as words:
    choise_word = random.choice(words.readlines())

palabra = choise_word.strip()
corta = cortar_palabra(palabra)

orden_letra = orden_ubicacion_letras(corta, palabra)
pos, letra = main_del_juego(corta)


completandonse_pal = []
intentos = len(orden_letra)
while len(pos) > 0:

    if "_" not in corta:
        print(print_win("()", "-___-"))
        print(f"\n\t\tGanaste !!!\n\tLa solucion es: {corta.capitalize()}\n\n")
        break

    if intentos == 0:
        ojo_string = "X "
        boca_string = "_---_"
        print(print_ahorcado(ojo_string, boca_string))
        print(f"\t\tFallate, lo mataste\n\tLa Palabra era: {palabra.capitalize()}\n\n")
        break
    else:
        print(print_ahorcado("()", "-----"))
    intentos -= 1

    if intentos == 0:
        print(f"\t{corta.capitalize()}\t\tIntento: último!!!")
    else:
        print(f"\t{corta.capitalize()}\t\tIntento: {intentos}")

    print("   Opciones: " + " ".join([str(i) for i in letra]))
    print()
    ingresado = input("\tLetra: ").split()


    if len(ingresado) > 1:
        print("Ingrese: Letra")
    elif ingresado == []:
        continue
    else:
        if ingresado[0].isalpha():
            if ingresado[0] in palabra:
                if ingresado[0] in letra:
                    letra.remove(ingresado[0])
                    intentos += 1
                for key_letter in orden_letra:
                    if ingresado[0] == list(key_letter.keys())[0]:
                        obt_posicion = list(key_letter.values())[0]
                        obt_posicion.sort()
                        algo = []
                        for iter in obt_posicion:
                            if algo == []:
                                algo.append(reemplazo_letras(iter, ingresado[0], corta))
                            else:
                                algo.append(reemplazo_letras(iter, ingresado[0], algo[-1]))
                        corta = algo[-1]
