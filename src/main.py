from telegram import BotCommand, Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    Application,
    ConversationHandler,
    MessageHandler,
    filters,
)
import gspread
import config

NAME = 0

START_COMMAND = "start"
START_DESCRIPTION = "Decile hola al bot"
START_REPLY = "Hola! 👋"

IS_PRESENT_COMMAND = "ispresent"
IS_PRESENT_DESCRIPTION = "Chequeá si una peli está en la lista"
IS_PRESENT_REPLY = "¿Qué peli estás buscando?"
IS_PRESENT_POSITIVE_RESULT = "Está en la lista ✅"
IS_PRESENT_NEGATIVE_RESULT = "No está en la lista ❌"

CANCEL_COMMAND = "cancel"
CANCEL_DESCRIPTION = "Terminá esta conversación"
CANCEL_REPLY = "Ok, te arrepentiste"


gc = gspread.service_account_from_dict(config.CREDENTIALS)
sheet = gc.open(config.SHEET_NAME).sheet1


async def post_init(app: Application):
    command_info = [
        BotCommand(START_COMMAND, START_DESCRIPTION),
        BotCommand(IS_PRESENT_COMMAND, IS_PRESENT_DESCRIPTION),
        BotCommand(CANCEL_COMMAND, CANCEL_DESCRIPTION),
    ]
    await app.bot.set_my_commands(commands=command_info)


async def start(update: Update, _context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(START_REPLY)


async def is_present(update: Update, _context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(IS_PRESENT_REPLY)
    return NAME


async def movie_name(update: Update, _context: ContextTypes.DEFAULT_TYPE):
    cell_list = sheet.findall(update.message.text)
    response = (
        IS_PRESENT_NEGATIVE_RESULT if not cell_list else IS_PRESENT_POSITIVE_RESULT
    )
    await update.message.reply_text(response)
    return ConversationHandler.END


async def cancel(update: Update, _context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(CANCEL_REPLY)
    return ConversationHandler.END


def main() -> None:
    app = ApplicationBuilder().token(config.BOT_TOKEN).post_init(post_init).build()

    start_handler = CommandHandler(START_COMMAND, start)
    is_present_handler = CommandHandler(IS_PRESENT_COMMAND, is_present)
    movie_name_handler = MessageHandler(~filters.COMMAND, movie_name)
    cancel_handler = CommandHandler(CANCEL_COMMAND, cancel)

    app.add_handler(start_handler)

    is_present_conversation_handler = ConversationHandler(
        entry_points=[is_present_handler],
        states={NAME: [movie_name_handler]},
        fallbacks=[cancel_handler],
    )
    app.add_handler(is_present_conversation_handler)

    match config.ENV:
        case "dev":
            print("Started bot polling")
            app.run_polling()
        case "prod":
            print("Started bot webhook")
            # app


if __name__ == "__main__":
    main()
