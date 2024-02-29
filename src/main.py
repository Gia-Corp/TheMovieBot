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


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hola!")


async def get_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¿Qué peli estás buscando?")
    return NAME


async def movie_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("La peli que se busca es: " + update.message.text)
    return ConversationHandler.END


async def post_init(application: Application):
    command_info = [
        BotCommand("start", "Saludá al bot"),
        BotCommand("getmovie", "Buscá una película por su nombre"),
    ]
    await application.bot.set_my_commands(commands=command_info)


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ok, no querés seguir buscando...")
    return ConversationHandler.END


NAME = 0


def main() -> None:
    load_dotenv()
    bot_token = os.environ["BOT_TOKEN"]
    application = ApplicationBuilder().token(bot_token).post_init(post_init).build()

    start_handler = CommandHandler("start", start)
    cancel_handler = CommandHandler("cancel", cancel)

    application.add_handler(start_handler)
    application.add_handler(cancel_handler)

    get_movie_handler = ConversationHandler(
        entry_points=[CommandHandler("getmovie", get_movie)],
        states={NAME: [MessageHandler(filters.TEXT, movie_name)]},
        fallbacks=[cancel_handler],
    )
    application.add_handler(get_movie_handler)

    print("🟢 Bot started successfully!")

    application.run_polling()


if __name__ == "__main__":
    main()
