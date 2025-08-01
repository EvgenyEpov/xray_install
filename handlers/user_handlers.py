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

    # Создаем задачи для всех серверов
    tasks = []
    for ip, password in all_hosts.items():
        task = asyncio.create_task(update_and_install_xray(message, ip, password))
        tasks.append(task)

    # Запускаем все задачи параллельно и ждем завершения
    await asyncio.gather(*tasks, return_exceptions=True)


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


@router.message(Command('install_full'))
async def handle_xray_full_deploy(message: Message):
    await message.answer("🚀 Запускаю полный деплой: обновление → установка Xray")

    all_hosts = host.ssh_bot.hosts

    # 1. Этап обновления
    update_results = {}

    async def update_server(ip: str, password: str):
        try:
            # Создаем заглушку для message с пустым методом answer
            class FakeMessage:
                async def answer(self, *args, **kwargs):
                    pass

            result = await process_server(ip, password, FakeMessage())
            update_results[ip] = {'status': True, 'message': "Сервер обновлён успешно"}
        except Exception as e:
            update_results[ip] = {'status': False, 'message': f"Сервер не обновлен, ошибка: {str(e)}"}

    await asyncio.gather(*[update_server(ip, pwd) for ip, pwd in all_hosts.items()])

    # Формируем отчет
    success_update = sum(1 for r in update_results.values() if r['status'])
    report = "\n".join(
        f"🟢 {ip} - {data['message']}" if data['status']
        else f"🔴 {ip} - {data['message']}"
        for ip, data in update_results.items()
    )

    await message.answer(
        f"🔷 <b>Результаты обновления ({success_update}/{len(all_hosts)}):</b>\n{report}"
    )

    # 2. Этап установки Xray
    if success_update == 0:
        await message.answer("❌ Нет успешно обновленных серверов!")
        return

    install_results = {}

    async def install_xray(ip: str, password: str):
        try:
            await update_and_install_xray(ip, password)
            install_results[ip] = {'status': True, 'message': "xray обновлён и установлен успешно"}
        except Exception as e:
            install_results[ip] = {'status': False, 'message': f"xray  не обновлён и  неустановлен, ошибка: {str(e)}"}

    await asyncio.gather(*[
        install_xray(ip, pwd)
        for ip, pwd in all_hosts.items()
        if update_results[ip]['status']
    ])

    # Итоговый отчет
    success_install = sum(1 for r in install_results.values() if r['status'])
    install_report = "\n".join(
        f"🟢 {ip} - {data['message']}" if data['status']
        else f"🔴 {ip} - {data['message']}"
        for ip, data in install_results.items()
    )

    await message.answer(
        f"🔷 <b>Результаты установки Xray ({success_install}/{success_update}):</b>\n{install_report}"
    )

    # Общий итог
    await message.answer(
        f"🏁 <b>Итоги деплоя:</b>\n"
        f"• Обновление: {success_update}/{len(all_hosts)}\n"
        f"• Установка Xray: {success_install}/{success_update}"
    )
