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


load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))


historico = []
entrada = None
gale = 0



def botoes():

    teclado = []

    linha = []


    for n in range(37):

        linha.append(
            InlineKeyboardButton(
                f"🎲 {n}",
                callback_data=f"num_{n}"
            )
        )

        if len(linha) == 5:
            teclado.append(linha)
            linha = []


    if linha:
        teclado.append(linha)


    teclado.append(
        [
            InlineKeyboardButton(
                "🟢 GREEN",
                callback_data="green"
            ),
            InlineKeyboardButton(
                "🔴 LOSS",
                callback_data="loss"
            )
        ]
    )


    teclado.append(
        [
            InlineKeyboardButton(
                "🔄 RESET",
                callback_data="reset"
            )
        ]
    )


    return InlineKeyboardMarkup(teclado)




def analisar():

    global entrada


    if len(historico) < 5:

        return None


    # análise simples por grupos

    entrada = [

        32,0,26,20,31,
        14,23,10,5

    ]


    return entrada





async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(

        "🔥 M7C7CO BOT 🔥\n\n"
        "Use /admin para abrir o painel."

    )





async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):


    if update.effective_user.id != ADMIN_ID:

        return


    await update.message.reply_text(

        "🔥 M7C7CO PAINEL 🔥\n\n"
        "Digite os números que saíram:",

        reply_markup=botoes()

    )





async def painel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    global gale


    query = update.callback_query

    await query.answer()



    if query.data.startswith("num_"):


        numero = int(
            query.data.replace(
                "num_",
                ""
            )
        )


        historico.append(numero)



        sinal = analisar()



        texto = (

            "🔥 M7C7CO ANALISADOR 🔥\n\n"

            f"🎲 Último giro: {numero}\n\n"

            f"📚 Histórico:\n{historico[-10:]}\n\n"

        )


        if sinal:


            texto += (

                "🎯 JOGADA 1 IDENTIFICADA\n\n"

                "Números análise:\n"

                "32 • 0 • 26 • 20 • 31\n\n"

                f"🟡 Gale atual: {gale}/3"

            )

        else:

            texto += "⏳ Aguardando padrão..."



        await query.edit_message_text(

            texto,

            reply_markup=botoes()

        )





    elif query.data == "green":


        await query.message.reply_text(

            "🟢 GREEN REGISTRADO ✅\n\n"
            "Novo ciclo iniciado."

        )


        resetar()



    elif query.data == "loss":


        await query.message.reply_text(

            "🔴 LOSS REGISTRADO\n\n"
            "Próximo ciclo."

        )


        resetar()



    elif query.data == "reset":


        resetar()


        await query.edit_message_text(

            "🔄 RESET COMPLETO\n\n"
            "Aguardando novos números.",

            reply_markup=botoes()

        )





def resetar():

    global historico
    global entrada
    global gale


    historico = []
    entrada = None
    gale = 0





def main():


    app = (

        Application

        .builder()

        .token(TOKEN)

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
            painel
        )

    )


    print(
        "🔥 M7C7CO ONLINE"
    )


    app.run_polling()




if __name__ == "__main__":

    main()
