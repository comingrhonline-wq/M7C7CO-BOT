import os

from dotenv import load_dotenv

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

from database import (
    criar_banco,
    salvar_numero,
    pegar_historico
)

from sinais import verificar_setor


load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🔥 M7C7CO BOT ONLINE 🔥\n\n"
        "Sistema iniciado.\n\n"
        "Digite /admin para abrir o painel."
    )



async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:

        await update.message.reply_text(
            "❌ Você não tem permissão."
        )

        return


    teclado = [

        [
            InlineKeyboardButton(
                "➕ Inserir Número",
                callback_data="inserir"
            )
        ],

        [
            InlineKeyboardButton(
                "📊 Estatísticas",
                callback_data="estatistica"
            )
        ],

        [
            InlineKeyboardButton(
                "📜 Histórico",
                callback_data="historico"
            )
        ]

    ]


    await update.message.reply_text(

        "🎯 M7C7CO PAINEL\n\n"
        "Escolha uma opção:",

        reply_markup=InlineKeyboardMarkup(teclado)

    )async def botoes(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()


    if query.data == "inserir":

        botoes_numeros = []

        linha = []

        for numero in range(37):

            linha.append(
                InlineKeyboardButton(
                    str(numero),
                    callback_data=f"num_{numero}"
                )
            )

            if len(linha) == 6:
                botoes_numeros.append(linha)
                linha = []

        if linha:
            botoes_numeros.append(linha)


        await query.edit_message_text(

            "🎯 M7C7CO\n\n"
            "Escolha o número que saiu:",

            reply_markup=InlineKeyboardMarkup(
                botoes_numeros
            )

        )


    elif query.data.startswith("num_"):

        numero = int(
            query.data.replace("num_", "")
        )

        await salvar_numero(numero)


        historico = await pegar_historico(50)

        numeros = [
            item[0]
            for item in historico
        ]


        resultado = verificar_setor(
            numeros
        )


        mensagem = (
            f"✅ Número registrado: {numero}\n\n"
            "📊 Situação atual:\n\n"
            f"🎯 Setor 1: {resultado['setor1']} giros\n"
            f"🎯 Setor 2: {resultado['setor2']} giros\n"
            f"🔥 Setor 3: {resultado['setor3']} giros"
        )


        await query.edit_message_text(
            mensagem
        )



    elif query.data == "historico":

        dados = await pegar_historico()

        texto = "📜 ÚLTIMOS NÚMEROS\n\n"

        for numero, data in dados:

            texto += f"🎲 {numero} - {data}\n"


        await query.edit_message_text(
            texto
        )



    elif query.data == "estatistica":

        dados = await pegar_historico(50)

        if not dados:

            await query.edit_message_text(
                "Ainda não existem números registrados."
            )

            return


        texto = (
            "📊 ESTATÍSTICAS M7C7CO\n\n"
            f"Jogadas analisadas: {len(dados)}"
        )


        await query.edit_message_text(
            texto
        )



async def iniciar():

    await criar_banco()



def main():

    app = Application.builder().token(TOKEN).build()


    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )


    app.add_handler(
        CommandHandler(
            "admin",
            admin
        )
    )


    app.add_handler(
        CallbackQueryHandler(
            botoes
        )
    )


    app.run_polling()



if __name__ == "__main__":

    import asyncio

    asyncio.run(
        iniciar()
    )

    main()
