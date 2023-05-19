def stringify():
    string_gify = f"""            1   2   3
          |---|---|---|
        1 | {dictado_listas["l1"][0]} | {dictado_listas["l1"][1]} | {dictado_listas["l1"][2]} |
        2 | {dictado_listas["l2"][0]} | {dictado_listas["l2"][1]} | {dictado_listas["l2"][2]} |
        3 | {dictado_listas["l3"][0]} | {dictado_listas["l3"][1]} | {dictado_listas["l3"][2]} |
          |---|---|---|
        """
    return string_gify


def gana_o_no(itm_X_or_O, lista_score):
    a = [dictado_listas["l1"][0], dictado_listas["l1"][1], dictado_listas["l1"][2]].count(itm_X_or_O)
    b = [dictado_listas["l2"][0], dictado_listas["l2"][1], dictado_listas["l2"][2]].count(itm_X_or_O)
    c = [dictado_listas["l3"][0], dictado_listas["l3"][1], dictado_listas["l3"][2]].count(itm_X_or_O)

    d = [dictado_listas["l1"][0], dictado_listas["l2"][0], dictado_listas["l3"][0]].count(itm_X_or_O)
    e = [dictado_listas["l1"][1], dictado_listas["l2"][1], dictado_listas["l3"][1]].count(itm_X_or_O)
    f = [dictado_listas["l1"][2], dictado_listas["l2"][2], dictado_listas["l3"][2]].count(itm_X_or_O)

    g = [dictado_listas["l1"][0], dictado_listas["l2"][1], dictado_listas["l3"][2]].count(itm_X_or_O)
    h = [dictado_listas["l3"][0], dictado_listas["l2"][1], dictado_listas["l1"][2]].count(itm_X_or_O)
    res = a,b,c,d,e,f,g,h
    lista_score.clear()
    lista_score.append(res)
    return [a,b,c,d,e,f,g,h], itm_X_or_O


def MainAgregarPosicion(ubicacion, lista, name_item, ticket_turno, score_game):
    item_Ganador = ""
    caracteres = ["O", "X"]
    location = int(ubicacion) - 1
    lista.pop(location)
    if ticket_turno % 2 == 0:
        lista.insert(location, caracteres[0])
        resultado = gana_o_no(caracteres[0], score_game)
    elif ticket_turno % 2 == 1:
        lista.insert(location, caracteres[1])
        resultado = gana_o_no(caracteres[1], score_game)
    itmm = {name_item: lista}
    dictado_listas.update(itmm)
    return stringify(), resultado



dictado_listas = {"l1": [" ", " ", " "], "l2": [" ", " ", " "], "l3": [" ", " ", " "]}
obtenido = ()
score = []
turno = 0
itm_win = ""
quebrar = True



print(stringify())
while True:

    if quebrar is False:
        print("\n")
        print(f"¡¡¡ Gana >>> {itm_win} <<< !!!")
        print("\n")
        break

    if turno >= 9:
        print("Nadie Gana")
        turno = 0
        score.clear()
        dictado_listas = {"l1": [" ", " ", " "], "l2": [" ", " ", " "], "l3": [" ", " ", " "]}
        break

    if turno % 2 == 0:
        print("Turno de:     O")
    elif turno % 2 == 1:
        print("Turno de:     X")

    coordenadas = input("Coordenadas:").split()
    if len(coordenadas) > 0 and len(coordenadas) <= 2 and len(coordenadas) != 1:
        for item_lista in dictado_listas:
            if coordenadas[0] in item_lista:
                if dictado_listas[item_lista][int(coordenadas[1]) - 1] == " ":
                    obtenido = MainAgregarPosicion(coordenadas[1], dictado_listas[item_lista], item_lista, turno, score)
                    print(obtenido[0])
                    print("\n")
                    if len(obtenido) >= 1:
                        if 3 in obtenido[1][0]:
                            itm_win = obtenido[1][1]
                            quebrar = False
                    turno += 1
                else:
                    print(obtenido[0])
                    print("\n")
                    continue
    else:
        print(stringify())
        continue
