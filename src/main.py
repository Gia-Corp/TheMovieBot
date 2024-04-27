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

BOT_STARTED_MESSAGE = "🟢 Bot started successfully!"
BOT_TOKEN_ENVIRONMENT_VARIABLE = "BOT_TOKEN"

load_dotenv()

credentials = {
    "type": os.environ["TYPE"],
    "project_id": os.environ["PROJECT_ID"],
    "private_key_id": os.environ["PRIVATE_KEY_ID"],
    "private_key": os.environ["PRIVATE_KEY"],
    "client_email": os.environ["CLIENT_EMAIL"],
    "client_id": os.environ["CLIENT_ID"],
    "auth_uri": os.environ["AUTH_URI"],
    "token_uri": os.environ["TOKEN_URI"],
    "auth_provider_x509_cert_url": os.environ["AUTH_PROVIDER_X509_CERT_URL"],
    "client_x509_cert_url": os.environ["CLIENT_X509_CERT_URL"],
}

gc = gspread.service_account_from_dict(credentials)
sheet = gc.open(SHEET_NAME).sheet1


async def post_init(app: Application):
    command_info = [
        BotCommand(START_COMMAND, START_DESCRIPTION),
        BotCommand(IS_PRESENT_COMMAND, IS_PRESENT_DESCRIPTION),
        BotCommand(CANCEL_COMMAND, CANCEL_DESCRIPTION),
    ]
    await app.bot.set_my_commands(commands=command_info)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(START_REPLY)


async def is_present(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(IS_PRESENT_REPLY)
    return NAME


async def movie_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cell_list = sheet.findall(update.message.text)
    response = (
        IS_PRESENT_NEGATIVE_RESULT if not cell_list else IS_PRESENT_POSITIVE_RESULT
    )
    await update.message.reply_text(response)
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(CANCEL_REPLY)
    return ConversationHandler.END


def main() -> None:
    bot_token = os.environ[BOT_TOKEN_ENVIRONMENT_VARIABLE]
    app = ApplicationBuilder().token(bot_token).post_init(post_init).build()

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

    print(BOT_STARTED_MESSAGE)

    app.run_polling()


if __name__ == "__main__":
    main()
