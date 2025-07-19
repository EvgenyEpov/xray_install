from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message

import asyncio

from aiogram.utils.i18n import I18n

from config_data.config import ConfigFile, load_config_file, ConfigSSH, load_config_ssh

from media.send_media.send_media import send_key2, send_media2, send_key_admin

from services.xray_install import update_and_install_xray, process_server

path: ConfigFile = load_config_file()
host: ConfigSSH = load_config_ssh()

router = Router()


@router.message(Command('xray_install'))
async def handle_xray_command(message: Message):
    await message.answer("Начинаю установку и настройку XRay на серверах...")

    all_hosts = {
        **host.ssh_bot.hosts,
    }

    # Обрабатываем серверы по одному
    for ip, password in all_hosts.items():
        result = await update_and_install_xray(ip, password)
        # Отправляем результат для каждого сервера отдельно
        await message.answer(result)


@router.message(Command('update_and_install'))
async def handle_xray_command(message: Message):
    await message.answer("Начинаю обновление на серверах...")

    all_hosts = {
        **host.ssh_bot.hosts
    }

    # Создаем задачи для всех серверов
    tasks = []
    for ip, password in all_hosts.items():
        task = asyncio.create_task(process_server(ip, password, message))
        tasks.append(task)

    # Можно добавить ожидание всех задач при необходимости
    await asyncio.gather(*tasks, return_exceptions=True)


@router.message(Command(commands='creating_keys'))
async def process_test(message: Message, bot: Bot, i18n: I18n):
    #     """
    #     функция делает рассылку с картинкой и реферальной ссылкой для приглашения новых людей
    #     :return: ничего не возвращает
    #     """
    parts = message.text.split()
    arg = parts[1] if len(parts) > 1 else None
