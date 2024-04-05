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

gc = gspread.service_account(filename=CREDENTIALS)
sheet = gc.open(SHEET_NAME).sheet1


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hola!")


async def is_present(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¿Qué peli estás buscando?")
    return NAME


async def movie_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cell_list = sheet.findall(update.message.text)
    response = MOVIE_NOT_FOUND if not cell_list else MOVIE_FOUND
    await update.message.reply_text(response)
    return ConversationHandler.END


async def post_init(app: Application):
    command_info = [
        BotCommand("start", "Saludá al bot"),
        BotCommand("ispresent", "Chequeá si una peli está en la lista"),
    ]
    await app.bot.set_my_commands(commands=command_info)


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ok, no querés seguir buscando...")
    return ConversationHandler.END


def main() -> None:
    load_dotenv()
    bot_token = os.environ["BOT_TOKEN"]

    app = ApplicationBuilder().token(bot_token).post_init(post_init).build()

    start_handler = CommandHandler("start", start)
    cancel_handler = CommandHandler("cancel", cancel)
    is_present_handler = CommandHandler("ispresent", is_present)
    movie_name_handler = MessageHandler(filters.TEXT, movie_name)

    app.add_handler(start_handler)
    app.add_handler(cancel_handler)

    is_present_conversation_handler = ConversationHandler(
        entry_points=[is_present_handler],
        states={NAME: [movie_name_handler]},
        fallbacks=[cancel_handler],
    )
    app.add_handler(is_present_conversation_handler)

    print("🟢 Bot started successfully!")

    app.run_polling()


if __name__ == "__main__":
    main()
