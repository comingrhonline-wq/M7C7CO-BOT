# M7C7CO - SISTEMA DE JOGADAS

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


def pertence_jogada(numero):

    if numero in JOGADA_1:
        return 1

    if numero in JOGADA_2:
        return 2

    if numero in JOGADA_3:
        return 3

    return 0



def analisar_historico(historico):

    atraso_j2 = 0
    atraso_j3 = 0


    for numero in historico:

        if numero in JOGADA_2:
            break

        atraso_j2 += 1



    for numero in historico:

        if numero in JOGADA_3:
            break

        atraso_j3 += 1



    # Nunca envia Jogada 1

    if atraso_j2 >= 3:

        return {

            "sinal": True,
            "jogada": 2,
            "numeros": JOGADA_2,
            "gales": 3

        }



    if atraso_j3 >= 2:

        return {

            "sinal": True,
            "jogada": 3,
            "numeros": JOGADA_3,
            "gales": 5

        }



    return {

        "sinal": False

    }





def verificar_resultado(numero, jogada):


    if jogada == 2:

        if numero in JOGADA_2:
            return "GREEN"



    if jogada == 3:

        if numero in JOGADA_3:
            return "GREEN"



    return "AGUARDANDO"
