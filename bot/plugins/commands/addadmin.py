from pyrogram import Client, filters
from pyrogram.types import Message

from bot.config import Config
from bot.utils.helpers import add_admin, get_admins, remove_admin


@Client.on_message(
    filters.command("adduser") & filters.private & filters.user(Config.OWNER_ID)
)
async def addadmin(client: Client, message: Message):
    if len(message.command) != 2:
        admins = await get_admins()
        text = "Authorized users:\n"
        for admin in admins:
            try:
                user = await client.get_users(admin)
                text += f" - {user.mention(style='md')} ({user.id})\n"
            except Exception:
                text += f" - {admin}\n"
        await message.reply_text(f"Usage: /adduser user_id\n\n{text}")
        return

    user_id = message.text.split(None, 1)[1]

    if user_id.isdigit():
        user_id = int(user_id)
    else:
        user_id = user_id.replace("@", "")

    try:
        user = await client.get_users(user_id)
    except Exception:
        await message.reply_text("Invalid user ID")
        return

    added = await add_admin(user_id)
    if added:
        await message.reply_text("Authorized user added successfully")
        await client.send_message(
            user_id,
            "You have been added as an authorized user by the bot owner. Now you can use the bot commands.",
        )
    else:
        await message.reply_text("This user is already an auth user")


@Client.on_message(
    filters.command("auth_users") & filters.private & filters.user(Config.OWNER_ID)
)
async def admins(client: Client, message: Message):
    admins = await get_admins()
    text = "Auth users:\n"
    for admin in admins:
        try:
            user = await client.get_users(admin)
            text += f" - {user.mention(style='md')} ({user.id})\n"
        except Exception:
            text += f" - {admin}\n"
    await message.reply_text(text)


@Client.on_message(
    filters.command("removeuser") & filters.private & filters.user(Config.OWNER_ID)
)
async def removeadmin(client: Client, message: Message):
    if len(message.command) != 2:
        admins = await get_admins()
        text = "Auth Users:\n"
        for admin in admins:
            try:
                user = await client.get_users(admin)
                text += f" - {user.mention(style='md')} ({user.id})\n"
            except Exception:
                text += f" - {admin}\n"
        await message.reply_text(f"Usage: /removeuser user_id\n\n{text}")
        return
    user_id = message.text.split(None, 1)[1]
    if user_id.isdigit():
        user_id = int(user_id)
    else:
        user_id = user_id.replace("@", "")

    removed = await remove_admin(user_id)
    if removed:
        await message.reply_text("Authorized user removed successfully")
        await client.send_message(
            user_id,
            "You have been removed as an authorized user by the bot owner. Now you can't use the bot commands.",
        )
    else:
        await message.reply_text("This user is not an admin")
