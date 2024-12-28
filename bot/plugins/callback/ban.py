from pyrogram import Client, filters
from bot.plugins.commands.user import user
from database import db

from pyrogram.types import CallbackQuery
from bot.utils import get_admins


@Client.on_callback_query(filters.regex(r"^ban_user"))
async def ban_user(bot: Client, query: CallbackQuery):
    user_id = int(query.data.split()[1])
    _user = await db.users.get_user(user_id)
    if not _user:
        return await query.answer("No user found with this id!")
    admins = await get_admins()

    if user_id in admins:
        return await query.answer("You can't ban an admin!", show_alert=True)

    if _user["banned"]:
        await db.users.update_user(user_id, {"banned": False})
        await query.answer("User unbanned successfully!")
    else:
        await db.users.update_user(user_id, {"banned": True})
        await query.answer("User banned successfully!")

    query.data = f"user {user_id}"
    await user(bot, query)
