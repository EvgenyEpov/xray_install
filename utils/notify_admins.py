import logging

from aiogram import Bot
from config_data.config import Config, load_config

admins: Config = load_config()


async def notify_admins(bot: Bot, text: str):
    for admin in admins.tg_bot.admin_ids:
        try:
            await bot.send_message(chat_id=admin, text=text)
        except Exception as err:
            logging.exception(err)
