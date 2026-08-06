SETORES = {

    "setor1": [
        32,0,26,20,31,14,23,10,5,2,25,17
    ],

    "setor2": [
        36,13,27,12,29,7,1,21,28,35,34,6,3
    ],

    "setor3": [
        24,16,33,15,19,4,9,22,18,8,30,11
    ]

}


def verificar_setor(historico):

    resultado = {}

    for nome, numeros in SETORES.items():

        contador = 0

        for numero in historico:

            if numero in numeros:
                break

            contador += 1

        resultado[nome] = contador

    return resultado
