# =========================================================
# M7C7CO - SISTEMA DE ANÁLISES
# =========================================================

from database import (
    JOGADAS,
    ROULETTE_ORDER,
    get_history,
    get_last_result,
    analyze,
    roulette_neighbors,
    get_jogadas_for_number
)


# =========================================================
# CORES DA ROLETA EUROPEIA
# =========================================================

RED_NUMBERS = {
    1, 3, 5, 7, 9, 12, 14, 16, 18,
    19, 21, 23, 25, 27, 30, 32, 34, 36
}

BLACK_NUMBERS = {
    2, 4, 6, 8, 10, 11, 13, 15, 17,
    20, 22, 24, 26, 28, 29, 31, 33, 35
}


# =========================================================
# IDENTIFICAR COR
# =========================================================

def get_color(number):

    if number == 0:
        return "GREEN"

    if number in RED_NUMBERS:
        return "RED"

    if number in BLACK_NUMBERS:
        return "BLACK"

    return "UNKNOWN"


# =========================================================
# ÚLTIMOS RESULTADOS
# =========================================================

def get_recent_results(limit=20):

    history = get_history(limit)

    return history


# =========================================================
# CONTAR CORES
# =========================================================

def count_colors(limit=100):

    history = get_history(limit)

    colors = {
        "RED": 0,
        "BLACK": 0,
        "GREEN": 0
    }

    for number in history:

        color = get_color(number)

        if color in colors:
            colors[color] += 1

    return colors


# =========================================================
# CONTAGEM DOS NÚMEROS
# =========================================================

def count_numbers(limit=1000):

    history = get_history(limit)

    counts = {}

    for number in history:

        if number not in counts:
            counts[number] = 0

        counts[number] += 1

    return counts


# =========================================================
# NÚMEROS MAIS FREQUENTES
# =========================================================

def hot_numbers(limit=1000, top=10):

    counts = count_numbers(limit)

    ordered = sorted(
        counts.items(),
        key=lambda item: item[1],
        reverse=True
    )

    return ordered[:top]


# =========================================================
# NÚMEROS MENOS FREQUENTES
# =========================================================

def cold_numbers(limit=1000, top=10):

    counts = count_numbers(limit)

    ordered = sorted(
        counts.items(),
        key=lambda item: item[1]
    )

    return ordered[:top]


# =========================================================
# AUSÊNCIAS DOS NÚMEROS
# =========================================================

def calculate_absences():

    history = get_history()

    if not history:
        return {}

    absences = {}

    reversed_history = list(reversed(history))

    for number in range(37):

        if number in reversed_history:

            position = reversed_history.index(number)

            absences[number] = position

        else:

            absences[number] = len(history)

    return absences


# =========================================================
# NÚMEROS MAIS AUSENTES
# =========================================================

def most_absent_numbers(top=10):

    absences = calculate_absences()

    ordered = sorted(
        absences.items(),
        key=lambda item: item[1],
        reverse=True
    )

    return ordered[:top]


# =========================================================
# ÚLTIMO NÚMERO
# =========================================================

def analyze_last_number():

    number = get_last_result()

    if number is None:

        return {
            "number": None,
            "color": None,
            "jogadas": [],
            "neighbors": []
        }

    return {
        "number": number,
        "color": get_color(number),
        "jogadas": get_jogadas_for_number(number),
        "neighbors": roulette_neighbors(number)
    }


# =========================================================
# ANALISAR JOGADAS
# =========================================================

def analyze_jogadas():

    result = analyze()

    return {
        "counts": result["counts"],
        "least": result["least"],
        "target_numbers": result["target_numbers"],
        "total": result["total"]
    }


# =========================================================
# NÚMEROS DAS JOGADAS
# =========================================================

def get_jogada_numbers(jogadas):

    numbers = []

    for jogada in jogadas:

        if jogada not in JOGADAS:
            continue

        for number in JOGADAS[jogada]:

            if number not in numbers:
                numbers.append(number)

    return numbers


# =========================================================
# ENCONTRAR REPETIÇÕES ENTRE JOGADAS
# =========================================================

def find_shared_numbers():

    shared = {}

    for number in range(37):

        jogadas = get_jogadas_for_number(number)

        if len(jogadas) > 1:

            shared[number] = jogadas

    return shared


# =========================================================
# ANALISAR VIZINHOS DOS ALVOS
# =========================================================

def analyze_target_neighbors():

    result = analyze()

    targets = result["target_numbers"]

    neighbors = []

    for number in targets:

        if number not in neighbors:
            neighbors.append(number)

        for neighbor in roulette_neighbors(number):

            if neighbor not in neighbors:
                neighbors.append(neighbor)

    return neighbors


# =========================================================
# GERAR RESUMO COMPLETO
# =========================================================

def full_analysis():

    state = analyze()

    last = analyze_last_number()

    colors = count_colors()

    hot = hot_numbers()

    cold = cold_numbers()

    absent = most_absent_numbers()

    target_neighbors = analyze_target_neighbors()

    return {

        "total": state["total"],

        "counts": state["counts"],

        "least": state["least"],

        "targets": state["target_numbers"],

        "target_neighbors": target_neighbors,

        "last": last,

        "colors": colors,

        "hot_numbers": hot,

        "cold_numbers": cold,

        "most_absent": absent
    }


# =========================================================
# FORMATAR RESUMO PARA O TELEGRAM
# =========================================================

def format_analysis():

    data = full_analysis()

    text = []

    text.append("🎰 M7C7CO — ANÁLISE")
    text.append("")
    text.append(f"📊 Total de giros: {data['total']}")

    text.append("")
    text.append("📋 JOGADAS")

    for jogada, quantidade in data["counts"].items():

        text.append(
            f"• {jogada}: {quantidade}"
        )

    text.append("")

    if data["least"]:

        text.append(
            "🎯 Menor frequência: "
            + ", ".join(data["least"])
        )

    if data["targets"]:

        text.append("")
        text.append("🔢 NÚMEROS ALVO")

        text.append(
            " ".join(
                str(number)
                for number in data["targets"]
            )
        )

    text.append("")

    if data["last"]["number"] is not None:

        text.append(
            f"🎲 Último: {data['last']['number']}"
        )

        text.append(
            f"🎨 Cor: {data['last']['color']}"
        )

        if data["last"]["jogadas"]:

            text.append(
                "📌 Jogada: "
                + ", ".join(data["last"]["jogadas"])
            )

        if data["last"]["neighbors"]:

            text.append(
                "🎯 Vizinhos: "
                + " ".join(
                    str(number)
                    for number in data["last"]["neighbors"]
                )
            )

    text.append("")

    text.append(
        f"🔴 Vermelhos: {data['colors']['RED']}"
    )

    text.append(
        f"⚫ Pretos: {data['colors']['BLACK']}"
    )

    text.append(
        f"🟢 Verdes: {data['colors']['GREEN']}"
    )

    return "\n".join(text)


# =========================================================
# TESTE DO ARQUIVO
# =========================================================

if __name__ == "__main__":

    print(format_analysis())
