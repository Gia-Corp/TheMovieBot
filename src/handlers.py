from telegram.ext import (
    Application,
)
import commands


async def post_init(app: Application):
    command_info = [
        commands.start_command,
        commands.get_movies_command,
        commands.create_movie_command,
        commands.is_present_command,
        commands.cancel_command,
    ]
    await app.bot.set_my_commands(commands=command_info)
