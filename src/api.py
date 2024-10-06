from fastapi import FastAPI, Request, Response
import config
# app = FastAPI()


# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

from contextlib import asynccontextmanager
from http import HTTPStatus
from telegram import Update
from telegram.ext import Application, CommandHandler
from telegram.ext._contexttypes import ContextTypes

# Initialize python telegram bot
ptb = (
    Application.builder()
    .updater(None)
    .token(config.BOT_TOKEN)
    .read_timeout(7)
    .get_updates_read_timeout(42)
    .build()
)


@asynccontextmanager
async def lifespan(_: FastAPI):
    await ptb.bot.setWebhook(
        config.KOYEB_PUBLIC_DOMAIN,
        config.WEBHOOK_PUBLIC_KEY,
        secret_token=config.WEBHOOK_UPDATE_TOKEN,
    )
    async with ptb:
        await ptb.start()
        yield
        await ptb.stop()


app = FastAPI(lifespan=lifespan)


@app.post("/updates")
async def process_update(request: Request):
    req = await request.json()
    update = Update.de_json(req, ptb.bot)
    await ptb.process_update(update)
    return Response(status_code=HTTPStatus.OK)


# Example handler
async def start(update, _: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    await update.message.reply_text("starting...")


ptb.add_handler(CommandHandler("start", start))
