from telegram import BotCommand, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, filters
import httpx
import config
from .cancel import cancel_handler

CREATE_MOVIE_COMMAND = "createmovie"
CREATE_MOVIE_DESCRIPTION = "Crear peli"
DEFAULT_MOVIES_ENDPOINT = "/movies"
API_CALL_TIMEOUT = 60.0

TITLE, DIRECTOR, YEAR, WATCHED = range(4)

create_movie_command = BotCommand(CREATE_MOVIE_COMMAND, CREATE_MOVIE_DESCRIPTION)


async def create_movie_in_api(endpoint=DEFAULT_MOVIES_ENDPOINT):
    url = f"{config.BACKEND_URL}{endpoint}"

    async with httpx.AsyncClient() as client:
        response = await client.post(url, timeout=API_CALL_TIMEOUT)
        response.raise_for_status()


async def create_movie(update, _):
    # await create_movie_in_api()

    await update.message.reply_text("¿Título de la peli?")
    return TITLE


create_movie_handler = CommandHandler(CREATE_MOVIE_COMMAND, create_movie)


async def movie_title(update, context):
    context.user_data["movie_title"] = update.message.text

    await update.message.reply_text("¿Quién la dirijo?")

    return DIRECTOR


async def movie_director(update, context):
    context.user_data["movie_director"] = update.message.text

    await update.message.reply_text("¿En qué año salió?")

    return YEAR


async def movie_year(update, context):
    context.user_data["movie_year"] = update.message.text

    keyboard = ReplyKeyboardMarkup(
        [["✔️ Sí", "❌ No"]], one_time_keyboard=True, resize_keyboard=True
    )
    await update.message.reply_text("¿Ya la viste?", reply_markup=keyboard)
    return WATCHED


async def handle_movie_watched(update, context):
    movie_watched = update.message.text

    await update.message.reply_text(
        f"TUS RESPUESTAS:\n\n"
        f"🎬 {context.user_data['movie_title']}\n"
        f"🎥 {context.user_data['movie_director']}\n"
        f"📅 {context.user_data['movie_year']}\n"
        f"👁 Viste: {movie_watched}",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END


create_movie_conversation_handler = ConversationHandler(
    entry_points=[create_movie_handler],
    states={
        TITLE: [MessageHandler(~filters.COMMAND, movie_title)],
        DIRECTOR: [MessageHandler(~filters.COMMAND, movie_director)],
        YEAR: [MessageHandler(~filters.COMMAND, movie_year)],
        WATCHED: [MessageHandler(~filters.COMMAND, handle_movie_watched)],
    },
    fallbacks=[cancel_handler],
)
