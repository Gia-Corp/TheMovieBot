from telegram import BotCommand
from telegram.ext import (
    CommandHandler,
)
import httpx
import config

GET_MOVIES_COMMAND = "getmovies"
GET_MOVIES_DESCRIPTION = "Ver pelis en la lista"
GET_MOVIES_REPLY = "[PLACEHOLDER] ACA VERIAS LAS PELIS EN LA LISTA"

get_movies_command = BotCommand(GET_MOVIES_COMMAND, GET_MOVIES_DESCRIPTION)


async def get_movies(update, _):
    url = f"{config.BACKEND_URL}/movies"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params={"page": 1, "size": 5}, timeout=30.0)
        response.raise_for_status()
        body = response.json()

    movies = body["movies"]
    text = "\n".join(
        [
            f"🎬 {movie['title']} ({movie['year']}) - {movie['director']}"
            for movie in movies
        ]
    )

    await update.message.reply_text(text)


get_movies_handler = CommandHandler(GET_MOVIES_COMMAND, get_movies)
