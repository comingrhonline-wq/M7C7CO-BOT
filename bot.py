import os
import asyncio

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
ultimo_sinal = None



def painel_botoes():

    teclado = []

    linha = []

    for numero in range(37):

        linha.append(
            InlineKeyboardButton(
                f"🎲 {numero}",
                callback_data=f"num_{numero}"
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
                "🗑 APAGAR SINAL",
                callback_data="apagar"
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




async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🔥 M7C7CO BOT ONLINE 🔥\n\n"
        "Use /admin para abrir o painel."
    )





async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:

        await update.message.reply_text(
            "❌ Sem permissão."
        )

        return



    await update.message.reply_text(

        "🔥 M7C7CO PAINEL 🔥\n\n"
        "🎯 Escolha o número que saiu:",

        reply_markup=painel_botoes()

    )






async def botoes(update: Update, context: ContextTypes.DEFAULT_TYPE):

    global ultimo_sinal


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



        texto = (

            "🔥 M7C7CO ANÁLISE 🔥\n\n"

            f"🎲 Último número: {numero}\n\n"

            f"📚 Histórico: {historico[-10:]}\n\n"

            "⏳ Analisando próxima entrada..."

        )


        await query.edit_message_text(

            texto,

            reply_markup=painel_botoes()

        )



        # sinal demonstrativo
        if len(historico) >= 5:


            ultimo_sinal = await context.bot.send_message(

                chat_id=query.message.chat.id,

                text=(

                    "🚨🔥 M7C7CO SINAL 🔥🚨\n\n"

                    "🎯 Entrada identificada\n\n"

                    "🎲 Proteção: 3 Gales\n\n"

                    "Aguardando resultado..."

                )

            )





    elif query.data == "green":


        await query.message.reply_text(

            "🟢🟢 GREEN CONFIRMADO 🟢🟢\n\n"
            "Entrada finalizada com sucesso."

        )




    elif query.data == "loss":


        await query.message.reply_text(

            "🔴 LOSS REGISTRADO 🔴\n\n"
            "Novo ciclo iniciado."

        )




    elif query.data == "reset":


        historico.clear()

        ultimo_sinal = None


        await query.edit_message_text(

            "🔄 RESET COMPLETO\n\n"
            "Novo ciclo iniciado.",

            reply_markup=painel_botoes()

        )




    elif query.data == "apagar":


        await query.message.delete()






async def iniciar(app):

    print(
        "🔥 M7C7CO ONLINE"
    )





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


    app.run_polling()





if __name__ == "__main__":

    main()
