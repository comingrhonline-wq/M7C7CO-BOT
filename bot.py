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

from sinais import analisar


load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))


historico = []

jogada_atual = None



CONTADOR = {

    1: 0,
    2: 0,
    3: 0

}



def menu_numeros():

    teclado = []

    linha = []


    for numero in range(37):

        linha.append(

            InlineKeyboardButton(

                f"🎲{numero}",

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




def texto_painel():


    return (

        "🔥 M7C7CO ANALYZER 🔥\n\n"

        "📊 PONTUAÇÃO\n"

        f"🎯 Jogada 1: {CONTADOR[1]}\n"

        f"🎯 Jogada 2: {CONTADOR[2]}\n"

        f"🎯 Jogada 3: {CONTADOR[3]}\n\n"

        "⏳ Aguardando números..."

    )






async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):


    await update.message.reply_text(

        "🔥 M7C7CO BOT 🔥\n\n"
        "Digite /admin"

    )





async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):


    if update.effective_user.id != ADMIN_ID:

        await update.message.reply_text(
            "❌ Sem acesso"
        )

        return



    await update.message.reply_text(

        texto_painel(),

        reply_markup=menu_numeros()

    )








async def botoes(update: Update, context: ContextTypes.DEFAULT_TYPE):


    global jogada_atual


    query = update.callback_query

    await query.answer()



    if query.data.startswith("num_"):


        numero = int(

            query.data.replace(
                "num_",
                ""
            )

        )



        resultado = analisar(numero)



        if resultado:


            jogada = resultado["jogada"]



            CONTADOR[jogada] += 1



            if jogada != 1:


                jogada_atual = jogada



                mensagem = (

                    "🔥🔥 M7C7CO SINAL 🔥🔥\n\n"

                    f"🎯 JOGADA {jogada}\n\n"

                    "🎲 ENTRADA LIBERADA\n\n"

                    "🛡 Proteção: 3 GALES"

                )


                await query.message.reply_text(

                    mensagem

                )



        await query.edit_message_text(

            texto_painel(),

            reply_markup=menu_numeros()

        )






    elif query.data == "green":


        await query.message.reply_text(

            "🟢 GREEN CONFIRMADO ✅\n\n"
            "Ciclo encerrado."

        )


        reset()



    elif query.data == "loss":


        await query.message.reply_text(

            "🔴 LOSS CONFIRMADO\n\n"
            "Novo ciclo iniciado."

        )


        reset()




    elif query.data == "reset":


        reset()


        await query.edit_message_text(

            texto_painel(),

            reply_markup=menu_numeros()

        )






def reset():


    global jogada_atual


    historico.clear()


    jogada_atual = None


    CONTADOR[1] = 0
    CONTADOR[2] = 0
    CONTADOR[3] = 0







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
            botoes
        )

    )


    print(
        "🔥 M7C7CO ONLINE"
    )


    app.run_polling()






if __name__ == "__main__":

    main()
