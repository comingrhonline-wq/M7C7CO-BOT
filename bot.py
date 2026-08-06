import os

from dotenv import load_dotenv

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

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


JOGADAS = {
    1: [32,0,26,20,31,14,23,10,5,2,25,17],
    2: [36,13,27,12,28,7,1,21,35,34,6,3],
    3: [24,16,33,15,19,4,9,22,18,8,30,11,29]
}



def menu():

    botoes=[]

    linha=[]

    for n in range(37):

        linha.append(
            InlineKeyboardButton(
                f"🎲{n}",
                callback_data=f"n_{n}"
            )
        )

        if len(linha)==6:
            botoes.append(linha)
            linha=[]


    if linha:
        botoes.append(linha)


    botoes.append(
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


    botoes.append(
        [
            InlineKeyboardButton(
                "🔄 RESET",
                callback_data="reset"
            )
        ]
    )


    return InlineKeyboardMarkup(botoes)



def analisar():


    atraso2=0
    atraso3=0


    for n in historico:

        if n in JOGADAS[2]:
            break

        atraso2+=1



    for n in historico:

        if n in JOGADAS[3]:
            break

        atraso3+=1



    if atraso2>=3:

        return 2



    if atraso3>=2:

        return 3



    return None




async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🔥 M7C7CO BOT 🔥\n\nDigite /admin"
    )





async def admin(update:Update,context:ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return


    await update.message.reply_text(

        "🔥 M7C7CO PAINEL 🔥\n\n"
        "Digite os números que saíram:",

        reply_markup=menu()

    )






async def botoes(update:Update,context:ContextTypes.DEFAULT_TYPE):

    query=update.callback_query

    await query.answer()


    if query.data.startswith("n_"):


        numero=int(
            query.data.replace(
                "n_",
                ""
            )
        )


        historico.insert(0,numero)


        jogada=analisar()



        if jogada:


            nums=JOGADAS[jogada]


            texto=(

                "🔥🔥 M7C7CO SINAL 🔥🔥\n\n"

                f"🎯 JOGADA {jogada}\n\n"

                "🎲 ENTRADA:\n\n"

                + " • ".join(map(str,nums))
                + "\n\n"

                "🛡 Proteção: 3 GALES"

            )


        else:


            texto=(

                "🔥 M7C7CO PAINEL 🔥\n\n"

                "⏳ Aguardando análise..."

            )



        await query.edit_message_text(

            texto,

            reply_markup=menu()

        )





    elif query.data=="green":


        await query.message.reply_text(

            "🟢 GREEN CONFIRMADO ✅\n\n"
            "Novo ciclo iniciado."

        )

        historico.clear()



    elif query.data=="loss":


        await query.message.reply_text(

            "🔴 LOSS REGISTRADO\n\n"
            "Novo ciclo."

        )

        historico.clear()




    elif query.data=="reset":


        historico.clear()


        await query.edit_message_text(

            "🔄 RESET FEITO\n\n"
            "Aguardando novos números.",

            reply_markup=menu()

        )






def main():


    app=(

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


    print("🔥 M7C7CO ONLINE")


    app.run_polling()



if __name__=="__main__":

    main()
    
