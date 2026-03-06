from telegram import BotCommand, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, filters
import httpx
import config
from .cancel import cancel_handler

ADD_MOVIE_COMMAND = "addmovie"
ADD_MOVIE_DESCRIPTION = "Nueva peli"
DEFAULT_MOVIES_ENDPOINT = "/movies"
API_CALL_TIMEOUT = 60.0

TITLE, DIRECTOR, YEAR, WATCHED = range(4)

add_movie_command = BotCommand(ADD_MOVIE_COMMAND, ADD_MOVIE_DESCRIPTION)


async def create_movie_in_api(movie):
    url = f"{config.BACKEND_URL}{DEFAULT_MOVIES_ENDPOINT}"

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=movie, timeout=API_CALL_TIMEOUT)
        response.raise_for_status()


async def add_movie(update, _):
    await update.message.reply_text("¿Título de la peli?")
    return TITLE


add_movie_handler = CommandHandler(ADD_MOVIE_COMMAND, add_movie)


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
        [["Sí", "No"]], one_time_keyboard=True, resize_keyboard=True
    )
    await update.message.reply_text("¿Ya la viste?", reply_markup=keyboard)
    return WATCHED


async def handle_movie_watched(update, context):
    movie_watched = update.message.text.lower() in ["✔️ sí", "sí", "si", "s"]

    movie = {
        "title": context.user_data['movie_title'],
        "director": context.user_data['movie_director'],
        "year": context.user_data['movie_year'],
        "watched": movie_watched
    }

    await create_movie_in_api(movie)

    await update.message.reply_text("Peli añadida exitosamente ✅",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END


add_movie_conversation_handler = ConversationHandler(
    entry_points=[add_movie_handler],
    states={
        TITLE: [MessageHandler(~filters.COMMAND, movie_title)],
        DIRECTOR: [MessageHandler(~filters.COMMAND, movie_director)],
        YEAR: [MessageHandler(~filters.COMMAND, movie_year)],
        WATCHED: [MessageHandler(~filters.COMMAND, handle_movie_watched)],
    },
    fallbacks=[cancel_handler],
)
