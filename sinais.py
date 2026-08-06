SETORES = {

    "setor1": [
        32, 0, 26, 20, 31, 14, 23,
        10, 5, 2, 25, 17
    ],

    "setor2": [
        36, 13, 27, 12, 29, 7, 1,
        21, 28, 35, 34, 6, 3
    ],

    "setor3": [
        24, 16, 33, 15, 19, 4, 9,
        22, 18, 8, 30, 11
    ]

}



def analisar(historico):

    resultado = {

        "setor1": 0,
        "setor2": 0,
        "setor3": 0,
        "sinal": False

    }


    for nome, numeros in SETORES.items():

        contador = 0


        for numero in historico:

            if numero in numeros:

                break

            contador += 1


        resultado[nome] = contador



    # Regra inicial do M7C7CO
    # quando algum setor fica 3 giros sem aparecer

    if (

        resultado["setor1"] >= 3

        or resultado["setor2"] >= 3

        or resultado["setor3"] >= 3

    ):

        resultado["sinal"] = True



    return resultado
