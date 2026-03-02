from telegram import BotCommand
from telegram.ext import (
    Application,
    ContextTypes,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)
from commands import start_command

NAME = 0

IS_PRESENT_COMMAND = "ispresent"
IS_PRESENT_DESCRIPTION = "Chequeá si una peli está en la lista"
IS_PRESENT_REPLY = "¿Qué peli estás buscando?"
IS_PRESENT_POSITIVE_RESULT = "Está en la lista ✅"
IS_PRESENT_NEGATIVE_RESULT = "No está en la lista ❌"

CANCEL_COMMAND = "cancel"
CANCEL_DESCRIPTION = "Terminá esta conversación"
CANCEL_REPLY = "Ok, te arrepentiste"


async def post_init(app: Application):
    command_info = [
        start_command,
        BotCommand(IS_PRESENT_COMMAND, IS_PRESENT_DESCRIPTION),
        BotCommand(CANCEL_COMMAND, CANCEL_DESCRIPTION),
    ]
    await app.bot.set_my_commands(commands=command_info)


async def is_present(update, _: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(IS_PRESENT_REPLY)
    return NAME


async def movie_name(update, _: ContextTypes.DEFAULT_TYPE):
    cell_list = None
    response = (
        IS_PRESENT_NEGATIVE_RESULT if not cell_list else IS_PRESENT_POSITIVE_RESULT
    )
    await update.message.reply_text(response)
    return ConversationHandler.END


async def cancel(update, _: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(CANCEL_REPLY)
    return ConversationHandler.END


is_present_handler = CommandHandler(IS_PRESENT_COMMAND, is_present)
movie_name_handler = MessageHandler(~filters.COMMAND, movie_name)
cancel_handler = CommandHandler(CANCEL_COMMAND, cancel)

is_present_conversation_handler = ConversationHandler(
    entry_points=[is_present_handler],
    states={NAME: [movie_name_handler]},
    fallbacks=[cancel_handler],
)
