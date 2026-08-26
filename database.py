import sqlite3
from pathlib import Path


# =========================================================
# CONFIGURAÇÃO DO BANCO
# =========================================================

DB_PATH = Path("m7c7co.db")


# =========================================================
# JOGADAS DA SUA TABELA
# =========================================================

JOGADAS = {
    "J1": [23, 8, 30, 22, 36, 23, 27, 6, 34],

    "J2": [5, 29, 16, 33, 2, 20, 14, 31, 9],

    "J3": [27, 25, 2, 22, 4, 29, 25, 32, 26],

    "J4": [22, 28, 29, 7, 28, 22, 35, 3],
}


# =========================================================
# ORDEM DA ROLETA EUROPEIA
# =========================================================

ROULETTE_ORDER = [
    0,
    32,
    15,
    19,
    4,
    21,
    2,
    25,
    17,
    34,
    6,
    27,
    13,
    36,
    11,
    30,
    8,
    23,
    10,
    5,
    24,
    16,
    33,
    1,
    20,
    14,
    31,
    9,
    22,
    18,
    29,
    7,
    28,
    12,
    35,
    3,
    26
]


# =========================================================
# BANCO DE DADOS
# =========================================================

def connect():

    conn = sqlite3.connect(DB_PATH)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            number INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()

    return conn


# =========================================================
# ADICIONAR RESULTADO
# =========================================================

def add_result(number):

    try:
        number = int(number)
    except (TypeError, ValueError):
        return False

    if number < 0 or number > 36:
        return False

    with connect() as conn:

        conn.execute(
            "INSERT INTO results(number) VALUES (?)",
            (number,)
        )

        conn.commit()

    return True


# =========================================================
# DESFAZER ÚLTIMO RESULTADO
# =========================================================

def undo_last():

    with connect() as conn:

        row = conn.execute(
            """
            SELECT id
            FROM results
            ORDER BY id DESC
            LIMIT 1
            """
        ).fetchone()

        if not row:
            return False

        conn.execute(
            "DELETE FROM results WHERE id = ?",
            (row[0],)
        )

        conn.commit()

    return True


# =========================================================
# RESET TOTAL
# =========================================================

def reset_all():

    with connect() as conn:

        conn.execute("DELETE FROM results")

        conn.commit()

    return True


# =========================================================
# PEGAR HISTÓRICO
# =========================================================

def get_history(limit=1000):

    with connect() as conn:

        rows = conn.execute(
            """
            SELECT number
            FROM results
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,)
        ).fetchall()

    return [row[0] for row in reversed(rows)]


# =========================================================
# ÚLTIMO RESULTADO
# =========================================================

def get_last_result():

    with connect() as conn:

        row = conn.execute(
            """
            SELECT number
            FROM results
            ORDER BY id DESC
            LIMIT 1
            """
        ).fetchone()

    if row:
        return row[0]

    return None


# =========================================================
# ESTADO ATUAL
# =========================================================

def get_state():

    with connect() as conn:

        total = conn.execute(
            "SELECT COUNT(*) FROM results"
        ).fetchone()[0]

        last = conn.execute(
            """
            SELECT number
            FROM results
            ORDER BY id DESC
            LIMIT 1
            """
        ).fetchone()

    return {
        "total": total,
        "last": last[0] if last else None
    }


# =========================================================
# ANALISAR AS 4 JOGADAS
# =========================================================

def analyze():

    history = get_history()

    counts = {
        "J1": 0,
        "J2": 0,
        "J3": 0,
        "J4": 0
    }

    # Cada resultado é comparado com as quatro jogadas.
    #
    # Se um número existir em duas jogadas,
    # ele conta nas duas.
    #
    # Isso é importante porque existem
    # números repetidos entre as jogadas.

    for number in history:

        for jogada, numeros in JOGADAS.items():

            if number in numeros:

                counts[jogada] += 1


    # =====================================================
    # ENCONTRAR A(S) MENOR(ES)
    # =====================================================

    menor = min(counts.values())

    least = [
        jogada
        for jogada, quantidade in counts.items()
        if quantidade == menor
    ]


    # =====================================================
    # PEGAR NÚMEROS DAS JOGADAS MENOS FREQUENTES
    # =====================================================

    target_numbers = []

    for jogada in least:

        for numero in JOGADAS[jogada]:

            if numero not in target_numbers:

                target_numbers.append(numero)


    return {

        "counts": counts,

        "least": least,

        "target_numbers": target_numbers,

        "total": len(history)
    }


# =========================================================
# VIZINHOS DA ROLETA
# =========================================================

def roulette_neighbors(number, each_side=2):

    if number not in ROULETTE_ORDER:
        return []

    position = ROULETTE_ORDER.index(number)

    neighbors = []

    # =====================================================
    # VIZINHOS DO LADO ESQUERDO
    # =====================================================

    for distance in range(-each_side, 0):

        neighbors.append(
            ROULETTE_ORDER[
                (position + distance) % len(ROULETTE_ORDER)
            ]
        )


    # =====================================================
    # VIZINHOS DO LADO DIREITO
    # =====================================================

    for distance in range(1, each_side + 1):

        neighbors.append(
            ROULETTE_ORDER[
                (position + distance) % len(ROULETTE_ORDER)
            ]
        )


    return neighbors


# =========================================================
# PEGAR VIZINHOS INCLUINDO O PRÓPRIO NÚMERO
# =========================================================

def roulette_sector(number, each_side=2):

    if number not in ROULETTE_ORDER:
        return []

    neighbors = roulette_neighbors(number, each_side)

    # Coloca o número principal junto dos vizinhos
    sector = [number] + neighbors

    # Remove possíveis duplicados
    result = []

    for n in sector:

        if n not in result:
            result.append(n)

    return result


# =========================================================
# VERIFICAR EM QUAL JOGADA O NÚMERO ESTÁ
# =========================================================

def get_jogadas_for_number(number):

    result = []

    for jogada, numeros in JOGADAS.items():

        if number in numeros:
            result.append(jogada)

    return result


# =========================================================
# ESTATÍSTICAS DE UM NÚMERO
# =========================================================

def number_stats(number):

    history = get_history()

    ocorrencias = history.count(number)

    jogadas = get_jogadas_for_number(number)

    vizinhos = roulette_neighbors(number)

    return {
        "number": number,
        "occurrences": ocorrencias,
        "jogadas": jogadas,
        "neighbors": vizinhos
    }


# =========================================================
# INICIALIZAR BANCO
# =========================================================

def init_database():

    with connect():
        pass


# =========================================================
# EXECUÇÃO DIRETA
# =========================================================

if __name__ == "__main__":

    init_database()

    print("===================================")
    print(" M7C7CO - DATABASE")
    print("===================================")

    state = get_state()

    print(f"Resultados registrados: {state['total']}")
    print(f"Último número: {state['last']}")

    analysis = analyze()

    print()
    print("Análise das jogadas:")
    print("---------------------")

    for jogada, quantidade in analysis["counts"].items():

        print(
            f"{jogada}: {quantidade}"
        )

    print()
    print("Jogada(s) menos frequente(s):")
    print(
        ", ".join(analysis["least"])
    )

    print()
    print("Números alvo:")

    print(
        analysis["target_numbers"]
    )

