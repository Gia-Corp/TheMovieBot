from telegram import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler
import httpx
import config

GET_MOVIES_COMMAND = "getmovies"
GET_MOVIES_DESCRIPTION = "Ver pelis en la lista"
GET_MOVIES_REPLY = "[PLACEHOLDER] ACA VERIAS LAS PELIS EN LA LISTA"

get_movies_command = BotCommand(GET_MOVIES_COMMAND, GET_MOVIES_DESCRIPTION)


async def get_movies_from_api(endpoint="/movies?page=1&size=5"):
    url = f"{config.BACKEND_URL}{endpoint}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=45.0)
        response.raise_for_status()
        body = response.json()

    return body["metadata"], body["movies"]


def create_reply_text(movies, metadata):
    movies_list = "\n".join(
        [
            f"🎬 {movie['title']} ({movie['year']}) {'✅' if movie['watched'] else ''}"
            for movie in movies
        ]
    )
    pagination_footer = f"\n\nPágina {metadata['page']}/{metadata['page_count']}"

    return movies_list + pagination_footer


async def get_movies(update, _):
    metadata, movies = await get_movies_from_api()

    text = create_reply_text(movies, metadata)

    await update.message.reply_text(text, reply_markup=build_keyboard(metadata))


def build_keyboard(pagination_metadata) -> InlineKeyboardMarkup:
    buttons = []

    if pagination_metadata["links"]["previous"]:
        buttons.append(
            InlineKeyboardButton(
                "◀️ Anterior", callback_data=pagination_metadata["links"]["previous"]
            )
        )
    if pagination_metadata["links"]["next"]:
        buttons.append(
            InlineKeyboardButton(
                "▶️ Siguiente", callback_data=pagination_metadata["links"]["next"]
            )
        )

    return InlineKeyboardMarkup([buttons])


async def handle_pagination(update, context):
    query = update.callback_query
    await query.answer()
    metadata, movies = await get_movies_from_api(query.data)
    text = create_reply_text(movies, metadata)

    await query.edit_message_text(
        text=text,
        reply_markup=build_keyboard(metadata),
    )

    context.drop_callback_data(query)


get_movies_handler = CommandHandler(GET_MOVIES_COMMAND, get_movies)

handle_pagination_handler = CallbackQueryHandler(handle_pagination)
