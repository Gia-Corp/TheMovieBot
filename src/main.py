import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from dotenv import load_dotenv

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ahora te contesto esto")


if __name__ == "__main__":
    load_dotenv()
    bot_token = os.environ["BOT_TOKEN"]
    application = ApplicationBuilder().token(bot_token).build()

    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)

    print("🟢 Bot started successfully!")

    application.run_polling()
