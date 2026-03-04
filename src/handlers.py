from telegram.ext import (
    Application,
)
from commands import (
    start_command,
    is_present_command,
    cancel_command,
    get_movies_command,
)


async def post_init(app: Application):
    command_info = [
        start_command,
        get_movies_command,
        is_present_command,
        cancel_command,
    ]
    await app.bot.set_my_commands(commands=command_info)
