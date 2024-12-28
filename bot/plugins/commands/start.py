from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot.config import Config, Script
from bot.utils.helpers import add_user


@Client.on_message(filters.command("start") & filters.private & filters.incoming)
@Client.on_callback_query(filters.regex("^start$"))
async def start(bot: Client, message: Message):
    await add_user(message.from_user.id)
    # owner buttons and link button
    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Owner", user_id=Config.OWNER_ID)],
            [
                InlineKeyboardButton(
                    "SOLANA NITRO PAIRS",
                    url="https://www.dextools.io/app/en/solana/token-race",
                )
            ],
        ]
    )
    text = Script.START_MESSAGE.format(mention=message.from_user.mention)
    await bot.reply(message, text, reply_markup=buttons, disable_web_page_preview=True)
