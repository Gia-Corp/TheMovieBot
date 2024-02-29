import os
from telegram import BotCommand, Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, Application
from dotenv import load_dotenv


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hola!")


async def get_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Acá va a aparecer un menú")


async def post_init(application: Application):
    command_info = [
        BotCommand("start", "Saludá al bot"),
        BotCommand("getmovie", "Buscá una película por su nombre"),
    ]
    await application.bot.set_my_commands(commands=command_info)


if __name__ == "__main__":
    load_dotenv()
    bot_token = os.environ["BOT_TOKEN"]
    application = ApplicationBuilder().token(bot_token).post_init(post_init).build()

    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)
    get_movie_handler = CommandHandler("getmovie", get_movie)
    application.add_handler(get_movie_handler)

    print("🟢 Bot started successfully!")

    application.run_polling()
