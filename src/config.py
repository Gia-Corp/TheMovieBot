from os import getenv
from dotenv import load_dotenv

load_dotenv()

# General config

ENV = getenv("ENV")

# Telegram config

BOT_TOKEN = getenv("BOT_TOKEN")
