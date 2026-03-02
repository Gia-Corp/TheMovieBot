from telegram import BotCommand
from telegram.ext import (
    CommandHandler,
)

START_COMMAND = "start"
START_DESCRIPTION = "Decile hola al bot"
START_REPLY = "Hola! 👋"

start_command = BotCommand(START_COMMAND, START_DESCRIPTION)


async def start(update, _):
    await update.message.reply_text(START_REPLY)


start_handler = CommandHandler(START_COMMAND, start)
