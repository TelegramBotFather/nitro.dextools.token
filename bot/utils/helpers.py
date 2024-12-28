import functools
import logging

from aiohttp import web
from pyrogram import Client, types

from database import db


async def get_admins():
    config = await db.config.get_config("ADMINS")
    return config["value"]


async def add_admin(user_id):
    config = await db.config.get_config("ADMINS")
    if config:
        admins = config["value"]
        if user_id not in admins:
            admins.append(user_id)
            await db.config.update_config("ADMINS", admins)
            return True
    else:
        await db.config.add_config("ADMINS", [user_id])
        return True

    return False


async def remove_admin(user_id):
    config = await db.config.get_config("ADMINS")
    if config:
        admins = config["value"]
        if user_id in admins:
            admins.remove(user_id)
            await db.config.update_config("ADMINS", admins)
            return True
    return False


async def start_webserver():
    routes = web.RouteTableDef()

    @routes.get("/", allow_head=True)
    async def root_route_handler(request):
        res = {
            "status": "running",
        }
        return web.json_response(res)

    async def web_server():
        web_app = web.Application(client_max_size=30000000)
        web_app.add_routes(routes)
        return web_app

    app = web.AppRunner(await web_server())
    await app.setup()
    await web.TCPSite(app, "127.0.0.1", 8000).start()
    logging.info("Web server started")


async def set_commands(app):
    COMMANDS = [
        types.BotCommand("start", "Start the bot."),
        types.BotCommand("admin", "Admin commands."),
    ]
    await app.set_bot_commands(COMMANDS)


async def add_user(user_id):
    user = await db.users.read(user_id)
    if user:
        return
    await db.users.create(user_id)
    return True


def check_admin(func):
    """Check if user is admin or not"""

    @functools.wraps(func)
    async def wrapper(client: Client, message):
        chat_id = getattr(message.from_user, "id", None)
        admins = await get_admins()
        buttons = types.InlineKeyboardMarkup(
            [
                [
                    types.InlineKeyboardButton(
                        "💬 Support", url=f"https://t.me/{client.owner.username}"
                    )
                ],
                [types.InlineKeyboardButton("🔙 Back", callback_data="start")],
            ]
        )
        if chat_id not in admins:
            return await client.reply(
                message,
                "You are not allowed to use this command.",
                reply_markup=buttons,
            )
        return await func(client, message)

    return wrapper


def safe_get(data, key, default=None):
    # Key = data.result.0.pair.0.name
    keys = key.split(".")
    for k in keys:
        try:
            data = data[int(k)] if k.isdigit() else data.get(k)
        except (IndexError, KeyError, AttributeError, TypeError):
            return default

    return default if data is None else data
