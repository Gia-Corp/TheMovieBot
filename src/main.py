from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Mirá cambié el texto dinámicamente"
    )


if __name__ == "__main__":
    bot_token = "6454892729:AAExNn5VsvyXAmua9s1D-fWy-YANvRgYqnE"
    application = ApplicationBuilder().token(bot_token).build()

    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)

    application.run_polling()
