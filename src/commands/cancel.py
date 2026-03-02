from telegram import BotCommand
from telegram.ext import (
    CommandHandler,
    ConversationHandler,
)

CANCEL_COMMAND = "cancel"
CANCEL_DESCRIPTION = "Terminá esta conversación"
CANCEL_REPLY = "Ok, te arrepentiste"

cancel_command = BotCommand(CANCEL_COMMAND, CANCEL_DESCRIPTION)


async def cancel(update, _):
    await update.message.reply_text(CANCEL_REPLY)
    return ConversationHandler.END


cancel_handler = CommandHandler(CANCEL_COMMAND, cancel)
