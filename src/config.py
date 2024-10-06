from os import getenv
from dotenv import load_dotenv

load_dotenv()

# General config

ENV = getenv("ENV")

# Telegram config

BOT_TOKEN = getenv("BOT_TOKEN")

KOYEB_PUBLIC_DOMAIN = getenv("KOYEB_PUBLIC_DOMAIN")

WEBHOOK_PUBLIC_KEY = getenv("WEBHOOK_PUBLIC_KEY")

WEBHOOK_UPDATE_TOKEN = getenv("WEBHOOK_UPDATE_TOKEN")
