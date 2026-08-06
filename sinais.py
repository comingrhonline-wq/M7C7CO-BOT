# M7C7CO - SISTEMA DE ANÁLISE DE JOGADAS

JOGADA_1 = [
    32, 0, 26, 20, 31,
    14, 23, 10, 5,
    2, 25, 17
]


JOGADA_2 = [
    36, 13, 27, 12,
    28, 7, 1, 21,
    35, 34, 6, 3
]


JOGADA_3 = [
    24, 16, 33, 15,
    19, 4, 9, 22,
    18, 8, 30, 11,
    29
]



def numero_da_jogada(numero):

    if numero in JOGADA_1:
        return 1

    if numero in JOGADA_2:
        return 2

    if numero in JOGADA_3:
        return 3

    return 0




def analisar(historico):

    resultado = {

        "jogada": None,
        "atraso": 0,
        "sinal": False,
        "numeros": []

    }


    ultima_jogada = numero_da_jogada(
        historico[0]
    )


    contador_j2 = 0
    contador_j3 = 0



    for numero in historico:


        jogada = numero_da_jogada(numero)



        if jogada == 2:

            break

        contador_j2 += 1




    for numero in historico:


        jogada = numero_da_jogada(numero)



        if jogada == 3:

            break

        contador_j3 += 1





    # REGRA JOGADA 2
    if contador_j2 >= 3:


        resultado["jogada"] = 2

        resultado["atraso"] = contador_j2

        resultado["sinal"] = True

        resultado["numeros"] = JOGADA_2

        return resultado





    # REGRA JOGADA 3
    if contador_j3 >= 2:


        resultado["jogada"] = 3

        resultado["atraso"] = contador_j3

        resultado["sinal"] = True

        resultado["numeros"] = JOGADA_3

        return resultado





    return resultado
