from telegram import BotCommand
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, filters
from .cancel import cancel_handler

IS_PRESENT_COMMAND = "ispresent"
IS_PRESENT_DESCRIPTION = "Chequeá si una peli está en la lista"
IS_PRESENT_REPLY = "¿Qué peli estás buscando?"
IS_PRESENT_POSITIVE_RESULT = "Está en la lista ✅"
IS_PRESENT_NEGATIVE_RESULT = "No está en la lista ❌"

NAME = 0

is_present_command = BotCommand(IS_PRESENT_COMMAND, IS_PRESENT_DESCRIPTION)


async def is_present(update, _):
    await update.message.reply_text(IS_PRESENT_REPLY)
    return NAME


is_present_handler = CommandHandler(IS_PRESENT_COMMAND, is_present)


async def movie_name(update, _):
    cell_list = None
    response = (
        IS_PRESENT_NEGATIVE_RESULT if not cell_list else IS_PRESENT_POSITIVE_RESULT
    )

    print(f"MOVIE NAME: {update.message.text}")

    await update.message.reply_text(response)
    return ConversationHandler.END


movie_name_handler = MessageHandler(~filters.COMMAND, movie_name)

is_present_conversation_handler = ConversationHandler(
    entry_points=[is_present_handler],
    states={NAME: [movie_name_handler]},
    fallbacks=[cancel_handler],
)
