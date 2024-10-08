from telegram.ext import Application
from telegram import Update
from fastapi import FastAPI, Request, Response
from contextlib import asynccontextmanager
from http import HTTPStatus
import config
import handlers

builder = (
    Application.builder()
    .token(config.BOT_TOKEN)
    .post_init(handlers.post_init)
    .read_timeout(7)
    .get_updates_read_timeout(42)
)

if config.BOT_MODE == "prod":
    builder.updater(None)

ptb = builder.build()
ptb.add_handler(handlers.start_handler)
ptb.add_handler(handlers.is_present_conversation_handler)

if config.BOT_MODE == "dev":
    print("🟣 Bot started in development mode")
    ptb.run_polling()


@asynccontextmanager
async def manage_bot_webhook(_: FastAPI):
    await ptb.bot.setWebhook(
        config.KOYEB_PUBLIC_DOMAIN + "/updates",
        config.WEBHOOK_PUBLIC_KEY,
        secret_token=config.WEBHOOK_UPDATE_TOKEN,
    )
    async with ptb:
        await ptb.start()
        yield
        await ptb.stop()


api = FastAPI(lifespan=manage_bot_webhook)


@api.get("/")
def give_status():
    return "The Movie Bot is currently active"


@api.post("/updates")
async def process_update(request: Request):
    req = await request.json()
    update = Update.de_json(req, ptb.bot)
    await ptb.process_update(update)
    return Response(status_code=HTTPStatus.OK)
