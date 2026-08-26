# =========================================================
# M7C7CO BOT
# BOT TELEGRAM PARA REGISTRO E ANÁLISE DE ROLETA
# =========================================================

import os
import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

from database import (
    add_result,
    undo_last,
    reset_all,
    get_history,
    get_state,
)

from analises import (
    get_color,
    full_analysis,
)


# =========================================================
# CONFIGURAÇÃO
# =========================================================

TOKEN = os.getenv("")

# Se quiser restringir o bot a um usuário específico,
# coloque o ID dele na variável ADMIN_ID do Railway.
ADMIN_ID = os.getenv("ADMIN_ID")


# =========================================================
# LOG
# =========================================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


# =========================================================
# VERIFICAR ADMIN
# =========================================================

def is_admin(update: Update):

    if not ADMIN_ID:
        return True

    try:
        admin_id = int(ADMIN_ID)
    except ValueError:
        return False

    user = update.effective_user

    if not user:
        return False

    return user.id == admin_id


# =========================================================
# MENSAGEM DE ACESSO NEGADO
# =========================================================

async def access_denied(update: Update):

    if update.callback_query:

        await update.callback_query.answer(
            "⛔ Você não tem permissão.",
            show_alert=True,
        )

    elif update.message:

        await update.message.reply_text(
            "⛔ Acesso restrito ao administrador."
        )


# =========================================================
# MENU PRINCIPAL
# =========================================================

def main_keyboard():

    keyboard = [

        [
            InlineKeyboardButton(
                "🎰 REGISTRAR NÚMERO",
                callback_data="numbers",
            )
        ],

        [
            InlineKeyboardButton(
                "📊 ANÁLISE",
                callback_data="analysis",
            ),

            InlineKeyboardButton(
                "📜 HISTÓRICO",
                callback_data="history",
            ),
        ],

        [
            InlineKeyboardButton(
                "↩️ DESFAZER",
                callback_data="undo",
            ),

            InlineKeyboardButton(
                "🔄 RESET",
                callback_data="reset",
            ),
        ],

    ]

    return InlineKeyboardMarkup(keyboard)


# =========================================================
# MENU DE NÚMEROS
# =========================================================

def numbers_keyboard():

    keyboard = []

    row = []

    for number in range(37):

        row.append(
            InlineKeyboardButton(
                str(number),
                callback_data=f"number:{number}",
            )
        )

        if len(row) == 6:

            keyboard.append(row)

            row = []

    if row:
        keyboard.append(row)

    keyboard.append(
        [
            InlineKeyboardButton(
                "⬅️ VOLTAR",
                callback_data="menu",
            )
        ]
    )

    return InlineKeyboardMarkup(keyboard)


# =========================================================
# MENU DE RESET
# =========================================================

def reset_keyboard():

    keyboard = [

        [
            InlineKeyboardButton(
                "✅ SIM, RESETAR",
                callback_data="confirm_reset",
            ),

            InlineKeyboardButton(
                "❌ CANCELAR",
                callback_data="menu",
            ),
        ]

    ]

    return InlineKeyboardMarkup(keyboard)


# =========================================================
# /START
# =========================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_admin(update):

        await access_denied(update)

        return

    state = get_state()

    text = (
        "🎰 *M7C7CO BOT*\n\n"
        "Sistema de registro e análise da roleta.\n\n"
        f"📊 Giros registrados: *{state['total']}*\n"
        f"🎲 Último número: *{state['last'] if state['last'] is not None else '-'}*\n\n"
        "Escolha uma opção:"
    )

    await update.message.reply_text(
        text,
        parse_mode="Markdown",
        reply_markup=main_keyboard(),
    )


# =========================================================
# /ADMIN
# =========================================================

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_admin(update):

        await access_denied(update)

        return

    state = get_state()

    text = (
        "👑 *PAINEL ADMINISTRATIVO*\n\n"
        f"📊 Total: *{state['total']}*\n"
        f"🎲 Último: *{state['last'] if state['last'] is not None else '-'}*\n\n"
        "Selecione uma operação:"
    )

    await update.message.reply_text(
        text,
        parse_mode="Markdown",
        reply_markup=main_keyboard(),
    )


# =========================================================
# MOSTRAR MENU DE NÚMEROS
# =========================================================

async def show_numbers(query):

    await query.edit_message_text(
        "🎰 *REGISTRAR RESULTADO*\n\n"
        "Selecione o número que saiu:",
        parse_mode="Markdown",
        reply_markup=numbers_keyboard(),
    )


# =========================================================
# REGISTRAR NÚMERO
# =========================================================

async def register_number(query, number):

    success = add_result(number)

    if not success:

        await query.answer(
            "❌ Número inválido.",
            show_alert=True,
        )

        return

    color = get_color(number)

    if color == "RED":
        emoji = "🔴"

    elif color == "BLACK":
        emoji = "⚫"

    else:
        emoji = "🟢"

    state = get_state()

    await query.answer(
        f"{emoji} Número {number} registrado!",
        show_alert=False,
    )

    text = (
        "✅ *RESULTADO REGISTRADO*\n\n"
        f"🎲 Número: *{number}*\n"
        f"{emoji} Cor: *{color}*\n\n"
        f"📊 Total de giros: *{state['total']}*\n\n"
        "Escolha o próximo número:"
    )

    await query.edit_message_text(
        text,
        parse_mode="Markdown",
        reply_markup=numbers_keyboard(),
    )


# =========================================================
# MOSTRAR ANÁLISE
# =========================================================

async def show_analysis(query):

    data = full_analysis()

    text = []

    text.append("📊 *ANÁLISE M7C7CO*")
    text.append("")

    text.append(
        f"🎰 Total de giros: *{data['total']}*"
    )

    text.append("")
    text.append("📋 *JOGADAS*")

    for jogada, quantidade in data["counts"].items():

        text.append(
            f"• {jogada}: *{quantidade}*"
        )

    text.append("")

    text.append(
        "🎯 Menor frequência: *"
        + ", ".join(data["least"])
        + "*"
    )

    text.append("")

    text.append("🔢 *NÚMEROS ALVO*")

    text.append(
        " ".join(
            str(number)
            for number in data["targets"]
        )
    )

    text.append("")

    if data["last"]["number"] is not None:

        text.append(
            f"🎲 Último: *{data['last']['number']}*"
        )

        text.append(
            f"🎨 Cor: *{data['last']['color']}*"
        )

        if data["last"]["jogadas"]:

            text.append(
                "📌 Jogada: "
                + ", ".join(data["last"]["jogadas"])
            )

        text.append(
            "🎯 Vizinhos: "
            + " ".join(
                str(number)
                for number in data["last"]["neighbors"]
            )
        )

    text.append("")

    text.append("🎨 *CORES*")

    text.append(
        f"🔴 Vermelho: {data['colors']['RED']}"
    )

    text.append(
        f"⚫ Preto: {data['colors']['BLACK']}"
    )

    text.append(
        f"🟢 Zero: {data['colors']['GREEN']}"
    )

    text.append("")

    text.append("🔥 *MAIS FREQUENTES*")

    if data["hot_numbers"]:

        for number, quantidade in data["hot_numbers"]:

            text.append(
                f"• {number}: {quantidade}x"
            )

    text.append("")

    text.append("❄️ *MAIS AUSENTES*")

    if data["most_absent"]:

        for number, ausencia in data["most_absent"]:

            text.append(
                f"• {number}: {ausencia} giro(s)"
            )

    keyboard = [
        [
            InlineKeyboardButton(
                "🔄 ATUALIZAR",
                callback_data="analysis",
            )
        ],
        [
            InlineKeyboardButton(
                "⬅️ VOLTAR",
                callback_data="menu",
            )
        ],
    ]

    await query.edit_message_text(
        "\n".join(text),
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


# =========================================================
# HISTÓRICO
# =========================================================

async def show_history(query):

    history = get_history(30)

    if not history:

        text = (
            "📜 *HISTÓRICO*\n\n"
            "Nenhum resultado registrado ainda."
        )

    else:

        recent = list(reversed(history))

        text = (
            "📜 *ÚLTIMOS RESULTADOS*\n\n"
        )

        text += " → ".join(
            str(number)
            for number in recent
        )

        text += (
            "\n\n"
            f"📊 Mostrando os últimos {len(recent)} resultados."
        )

    keyboard = [
        [
            InlineKeyboardButton(
                "🔄 ATUALIZAR",
                callback_data="history",
            )
        ],
        [
            InlineKeyboardButton(
                "⬅️ VOLTAR",
                callback_data="menu",
            )
        ],
    ]

    await query.edit_message_text(
        text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


# =========================================================
# DESFAZER
# =========================================================

async def do_undo(query):

    success = undo_last()

    if success:

        await query.answer(
            "↩️ Último resultado removido."
        )

    else:

        await query.answer(
            "⚠️ Não existem resultados para desfazer.",
            show_alert=True,
        )

    state = get_state()

    text = (
        "↩️ *DESFAZER*\n\n"
        "Última operação processada.\n\n"
        f"📊 Total: *{state['total']}*\n"
        f"🎲 Último: *{state['last'] if state['last'] is not None else '-'}*"
    )

    await query.edit_message_text(
        text,
        parse_mode="Markdown",
        reply_markup=main_keyboard(),
    )


# =========================================================
# RESET
# =========================================================

async def ask_reset(query):

    await query.edit_message_text(
        "⚠️ *ATENÇÃO*\n\n"
        "Isso apagará todo o histórico da roleta.\n\n"
        "Tem certeza que deseja continuar?",
        parse_mode="Markdown",
        reply_markup=reset_keyboard(),
    )


async def confirm_reset(query):

    reset_all()

    await query.answer(
        "🔄 Histórico resetado!"
    )

    await query.edit_message_text(
        "✅ *RESET CONCLUÍDO*\n\n"
        "Todo o histórico foi apagado.\n"
        "O próximo giro começará um novo ciclo.",
        parse_mode="Markdown",
        reply_markup=main_keyboard(),
    )


# =========================================================
# CALLBACK DOS BOTÕES
# =========================================================

async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    if not is_admin(update):

        await access_denied(update)

        return

    await query.answer()

    data = query.data

    # -----------------------------------------------------
    # MENU
    # -----------------------------------------------------

    if data == "menu":

        state = get_state()

        text = (
            "🎰 *M7C7CO BOT*\n\n"
            f"📊 Giros: *{state['total']}*\n"
            f"🎲 Último: *{state['last'] if state['last'] is not None else '-'}*\n\n"
            "Escolha uma opção:"
        )

        await query.edit_message_text(
            text,
            parse_mode="Markdown",
            reply_markup=main_keyboard(),
        )

        return

    # -----------------------------------------------------
    # NÚMEROS
    # -----------------------------------------------------

    if data == "numbers":

        await show_numbers(query)

        return

    # -----------------------------------------------------
    # REGISTRAR NÚMERO
    # -----------------------------------------------------

    if data.startswith("number:"):

        try:

            number = int(
                data.split(":")[1]
            )

        except (IndexError, ValueError):

            await query.answer(
                "❌ Número inválido.",
                show_alert=True,
            )

            return

        await register_number(
            query,
            number
        )

        return

    # -----------------------------------------------------
    # ANÁLISE
    # -----------------------------------------------------

    if data == "analysis":

        await show_analysis(query)

        return

    # -----------------------------------------------------
    # HISTÓRICO
    # -----------------------------------------------------

    if data == "history":

        await show_history(query)

        return

    # -----------------------------------------------------
    # DESFAZER
    # -----------------------------------------------------

    if data == "undo":

        await do_undo(query)

        return

    # -----------------------------------------------------
    # RESET
    # -----------------------------------------------------

    if data == "reset":

        await ask_reset(query)

        return

    # -----------------------------------------------------
    # CONFIRMAR RESET
    # -----------------------------------------------------

    if data == "confirm_reset":

        await confirm_reset(query)

        return


# =========================================================
# TRATAMENTO DE ERROS
# =========================================================

async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE
):

    logger.error(
        "Erro durante execução do bot:",
        exc_info=context.error,
    )


# =========================================================
# INICIAR BOT
# =========================================================

def main():

    if not TOKEN:

        raise RuntimeError(
            "BOT_TOKEN não configurado."
        )

    application = (
        Application.builder()
        .token(TOKEN)
        .build()
    )

    application.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    application.add_handler(
        CommandHandler(
            "admin",
            admin
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            button_handler
        )
    )

    application.add_error_handler(
        error_handler
    )

    print("====================================")
    print(" M7C7CO BOT INICIADO")
    print("====================================")

    application.run_polling(
        drop_pending_updates=True
    )


# =========================================================
# EXECUTAR
# =========================================================

if __name__ == "__main__":
    main()
