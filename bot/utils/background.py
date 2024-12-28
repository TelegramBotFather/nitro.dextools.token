import logging

from dextools_python import DextoolsAPIV2
from pyrogram import Client

from bot.config import Config
from database import db

from bot.utils.dextools import get_token_race

dextools = DextoolsAPIV2(Config.DEXTOOLS_API_KEY, plan="standard")


async def process_new_pairs(app):
    first_run = False
    try:
        pairs = await get_pairs_by_api()

    except Exception as e:
        logging.error(f"Error fetching pairs: {e}")
        return

    message_to_send = await make_text_message(pairs)

    if not message_to_send:
        return

    if not await db.hotpairs.filter_document({}):
        first_run = True
        logging.info("First run detected")

    for pair in pairs:
        if not await db.hotpairs.filter_document({"ca": pair["ca"]}):
            await db.hotpairs.create(pair["ca"])

    if first_run:
        logging.info("Skipping message sending on first run")
        return

    if "🔥" in message_to_send and Config.MAIN_CHAT["new_token_topic_id"]:
        logging.info(
            f"New token detected, sending to topic {Config.MAIN_CHAT['new_token_topic_id']}"
        )
        await send_messages(
            app,
            Config.MAIN_CHAT["chat_id"],
            message_to_send,
            Config.MAIN_CHAT["new_token_topic_id"],
        )


async def get_pairs_by_api():
    hot_pools = await get_token_race()
    pairs = []
    if "data" not in hot_pools:
        logging.error(f"Invalid response from DexTools API: {hot_pools}")
        raise Exception("Error fetching hot pairs")

    for pool in hot_pools["data"]["result"]:
        address = pool["mainToken"]["address"]

        if pool["chain"] != "solana":
            continue

        if not address:
            logging.warning(f"Skipping pool due to missing data: {pool}")
            continue

        name = pool["mainToken"]["name"]
        symbol = pool["mainToken"]["symbol"]

        pairs.append({"ca": address, "name": name, "symbol": symbol})
    return pairs


async def make_text_message(pairs):
    # https://www.dextools.io/app/en/solana/pair-explorer/FCEnSxyJfRSKsz6tASUENCsfGwKgkH6YuRn1AMmyHhZn
    text = f"TOP {len(pairs)} SOL NITRO PAIRS:\n"
    for i, pair in enumerate(pairs):
        # Add fire emoji if the pair is new
        emoji = "🔥 " if await is_new(pair["ca"]) else ""
        # text += f"{i+1}. {pair['name']}/SOL{emoji}\n"
        symbol = pair["symbol"].strip().upper().replace("/", "")
        text += f"{i+1}. [{symbol}/SOL](https://www.dextools.io/app/en/solana/pair-explorer/{pair['ca']}){emoji}\n"
    return text


async def send_messages(app: Client, channel_id, message, topic_id):
    channel_id = int(channel_id)
    try:
        await app.floodwait_handler(
            app.send_message,
            channel_id,
            message,
            disable_web_page_preview=True,
            reply_to_message_id=topic_id,
        )
    except Exception as e:
        logging.error(f"Failed to send message to channel {channel_id}: {str(e)}")


async def is_new(address):
    return not bool(await db.hotpairs.filter_document({"ca": address}))
