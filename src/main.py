import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from dotenv import load_dotenv


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Ya quité el token del código 2.0!"
    )


if __name__ == "__main__":
    load_dotenv()
    bot_token = os.environ["BOT_TOKEN"]
    application = ApplicationBuilder().token(bot_token).build()

    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)

    application.run_polling()
