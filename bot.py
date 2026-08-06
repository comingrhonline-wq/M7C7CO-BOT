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


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 M7C7CO BOT ONLINE 🔥\n\n"
        "Sistema iniciado com sucesso.\n"
        "Digite /admin para abrir o painel."
    )


async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id != ADMIN_ID:
        await update.message.reply_text(
            "❌ Acesso negado."
        )
        return

    teclado = [
        [
            InlineKeyboardButton(
                "➕ Inserir Número",
                callback_data="numero"
            )
        ],
        [
            InlineKeyboardButton(
                "📊 Estatísticas",
                callback_data="stats"
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
        "━━━━━━━━━━━━━━\n"
        "🎯 M7C7CO PAINEL\n"
        "━━━━━━━━━━━━━━\n\n"
        "Escolha uma opção:",
        reply_markup=InlineKeyboardMarkup(teclado)
    )


async def botoes(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data == "numero":
        await query.edit_message_text(
            "🔢 Escolha o número que saiu:"
        )

    elif query.data == "stats":
        await query.edit_message_text(
            "📊 Estatísticas\n\n"
            "Ainda iniciando o monitoramento."
        )

    elif query.data == "historico":
        await query.edit_message_text(
            "📜 Histórico vazio."
        )


def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CommandHandler("admin", admin)
    )

    app.add_handler(
        CallbackQueryHandler(botoes)
    )

    print("🔥 M7C7CO BOT iniciado")

    app.run_polling()


if __name__ == "__main__":
    main()
