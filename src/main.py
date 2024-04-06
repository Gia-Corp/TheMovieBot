import os
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
from dotenv import load_dotenv
import gspread

NAME = 0

SHEET_NAME = "test_movieproject"
CREDENTIALS = "credentials.json"

MOVIE_FOUND = "Está en la lista ✅"
MOVIE_NOT_FOUND = "No está en la lista ❌"

START_COMMAND = "start"
START_REPLY = "Hola!"
START_DESCRIPTION = "Saludá al bot"
IS_PRESENT_COMMAND = "ispresent"
IS_PRESENT_REPLY = "¿Qué peli estás buscando?"
IS_PRESENT_DESCRIPTION = "Chequeá si una peli está en la lista"
CANCEL_COMMAND = "cancel"
CANCEL_REPLY = "Ok, no querés seguir buscando..."

BOT_STARTED_MESSAGE = "🟢 Bot started successfully!"
BOT_TOKEN_ENVIRONMENT_VARIABLE = "BOT_TOKEN"

gc = gspread.service_account(filename=CREDENTIALS)
sheet = gc.open(SHEET_NAME).sheet1


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(START_REPLY)


async def is_present(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(IS_PRESENT_REPLY)
    return NAME


async def movie_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cell_list = sheet.findall(update.message.text)
    response = MOVIE_NOT_FOUND if not cell_list else MOVIE_FOUND
    await update.message.reply_text(response)
    return ConversationHandler.END


async def post_init(app: Application):
    command_info = [
        BotCommand(START_COMMAND, START_DESCRIPTION),
        BotCommand(IS_PRESENT_COMMAND, IS_PRESENT_DESCRIPTION),
    ]
    await app.bot.set_my_commands(commands=command_info)


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(CANCEL_REPLY)
    return ConversationHandler.END


def main() -> None:
    load_dotenv()
    bot_token = os.environ[BOT_TOKEN_ENVIRONMENT_VARIABLE]

    app = ApplicationBuilder().token(bot_token).post_init(post_init).build()

    start_handler = CommandHandler(START_COMMAND, start)
    cancel_handler = CommandHandler(CANCEL_COMMAND, cancel)
    is_present_handler = CommandHandler(IS_PRESENT_COMMAND, is_present)
    movie_name_handler = MessageHandler(filters.TEXT, movie_name)

    app.add_handler(start_handler)
    app.add_handler(cancel_handler)

    is_present_conversation_handler = ConversationHandler(
        entry_points=[is_present_handler],
        states={NAME: [movie_name_handler]},
        fallbacks=[cancel_handler],
    )
    app.add_handler(is_present_conversation_handler)

    print(BOT_STARTED_MESSAGE)

    app.run_polling()


if __name__ == "__main__":
    main()
