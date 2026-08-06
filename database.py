import aiosqlite
from datetime import datetime

DB = "m7c7co.db"


async def criar_banco():
    async with aiosqlite.connect(DB) as banco:
        await banco.execute("""
        CREATE TABLE IF NOT EXISTS historico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero INTEGER,
            data TEXT
        )
        """)

        await banco.commit()


async def salvar_numero(numero):
    async with aiosqlite.connect(DB) as banco:
        await banco.execute(
            """
            INSERT INTO historico(numero, data)
            VALUES (?, ?)
            """,
            (
                numero,
                datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            )
        )

        await banco.commit()


async def pegar_historico(limite=20):
    async with aiosqlite.connect(DB) as banco:
        cursor = await banco.execute(
            """
            SELECT numero, data
            FROM historico
            ORDER BY id DESC
            LIMIT ?
            """,
            (limite,)
        )

        dados = await cursor.fetchall()

        return dados
