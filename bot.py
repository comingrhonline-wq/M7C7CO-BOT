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
    resetar_dados,
    pegar_historico
)

from sinais import analisar


load_dotenv()


TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
GRUPO_ID = os.getenv("GROUP_ID")



def teclado_numeros():

    teclado = []
    linha = []

    for numero in range(37):

        linha.append(
            InlineKeyboardButton(
                str(numero),
                callback_data=f"num_{numero}"
            )
        )

        if len(linha) == 6:
            teclado.append(linha)
            linha = []


    if linha:
        teclado.append(linha)


    teclado.append(
        [
            InlineKeyboardButton(
                "🔄 RESET",
                callback_data="reset"
            )
        ]
    )


    return InlineKeyboardMarkup(teclado)




async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🔥 M7C7CO BOT ONLINE 🔥\n\n"
        "Digite /admin para abrir o painel."
    )




async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:

        await update.message.reply_text(
            "❌ Sem permissão."
        )

        return


    await update.message.reply_text(

        "🎯 M7C7CO PAINEL\n\n"
        "Escolha o número que saiu:",

        reply_markup=teclado_numeros()

    )





async def botoes(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()



    if query.data == "reset":

        await resetar_dados()


        await query.edit_message_text(

            "🔄 M7C7CO RESETADO\n\n"
            "Novo ciclo iniciado.",

            reply_markup=teclado_numeros()

        )

        return




    if query.data.startswith("num_"):


        numero = int(
            query.data.replace(
                "num_",
                ""
            )
        )


        await salvar_numero(numero)


        dados = await pegar_historico(50)


        numeros = [

            item[0]

            for item in dados

        ]


        resultado = analisar(numeros)



        painel = (

            "🎯 M7C7CO PAINEL\n\n"

            f"Último número: {numero}\n\n"

            f"📌 Setor 1: {resultado['setor1']}\n"

            f"📌 Setor 2: {resultado['setor2']}\n"

            f"📌 Setor 3: {resultado['setor3']}"

        )


        await query.edit_message_text(

            painel,

            reply_markup=teclado_numeros()

        )



        if resultado["sinal"] and GRUPO_ID:


            await context.bot.send_message(

                chat_id=GRUPO_ID,

                text=(

                    "🔥🔥 M7C7CO SINAL 🔥🔥\n\n"

                    "🎯 Entrada identificada\n\n"

                    f"Último número: {numero}\n\n"

                    "🚀 M7C7CO"

                )

            )






async def iniciar(app):

    await criar_banco()





def main():


    app = (

        Application

        .builder()

        .token(TOKEN)

        .post_init(iniciar)

        .build()

    )



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


    print(
        "🔥 M7C7CO BOT ONLINE"
    )


    app.run_polling()





if __name__ == "__main__":

    main()
