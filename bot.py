import os

from dotenv import load_dotenv

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

from sinais import (
    analisar_historico,
    verificar_resultado,
    pertence_jogada
)


load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))


historico = []

sinal_atual = None

gale = 0



# números da roleta europeia para visual
VERMELHOS = {
    1,3,5,7,9,12,14,16,18,
    19,21,23,25,27,30,32,34,36
}



def cor_numero(numero):

    if numero == 0:
        return "🟢"

    if numero in VERMELHOS:
        return "🔴"

    return "⚫"




def teclado():

    linhas = []

    linha = []


    for n in range(37):

        linha.append(

            InlineKeyboardButton(

                f"{cor_numero(n)}{n}",

                callback_data=f"num_{n}"

            )

        )


        if len(linha) == 6:

            linhas.append(linha)

            linha = []



    if linha:
        linhas.append(linha)



    return InlineKeyboardMarkup(linhas)




def painel():

    return (

        "🔥 M7C7CO ANALYZER 🔥\n\n"

        "🎯 Sistema ativo\n"

        "🟢 Zero\n"
        "🔴 Vermelho\n"
        "⚫ Preto\n\n"

        "Digite o número que saiu:"

    )





async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(

        "🔥 M7C7CO BOT 🔥\n\n"
        "Use /admin"

    )





async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:

        await update.message.reply_text(
            "❌ Sem permissão"
        )

        return



    await update.message.reply_text(

        painel(),

        reply_markup=teclado()

    )







async def numeros(update: Update, context: ContextTypes.DEFAULT_TYPE):

    global sinal_atual
    global gale


    query = update.callback_query

    await query.answer()



    numero = int(

        query.data.replace(
            "num_",
            ""
        )

    )



    historico.insert(0, numero)



    # verifica resultado se existe sinal

    if sinal_atual:


        resultado = verificar_resultado(

            numero,

            sinal_atual

        )


        if resultado == "GREEN":


            await query.message.reply_text(

                "🟢 GREEN CONFIRMADO ✅\n\n"

                f"Jogada {sinal_atual}\n"

                f"Confirmou no Gale {gale}"

            )


            sinal_atual = None

            gale = 0



        else:


            gale += 1


            limite = 3


            if sinal_atual == 3:

                limite = 5



            if gale >= limite:


                await query.message.reply_text(

                    "🔴 LOSS CONFIRMADO\n\n"

                    f"Jogada {sinal_atual}\n"

                    "Novo ciclo."

                )


                sinal_atual = None

                gale = 0



    else:


        analise = analisar_historico(

            historico

        )


        if analise["sinal"]:


            sinal_atual = analise["jogada"]

            gale = 0


            numeros = " • ".join(

                map(

                    str,

                    analise["numeros"]

                )

            )


            await query.message.reply_text(

                "🔥🔥 M7C7CO SINAL 🔥🔥\n\n"

                f"🎯 JOGADA {sinal_atual}\n\n"

                "🎲 ENTRADA:\n\n"

                f"{numeros}\n\n"

                f"🛡 GALES: {analise['gales']}"

            )



    await query.edit_message_text(

        painel(),

        reply_markup=teclado()

    )






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

            numeros

        )

    )


    print(

        "🔥 M7C7CO ONLINE"

    )


    app.run_polling()





if __name__ == "__main__":

    main()
