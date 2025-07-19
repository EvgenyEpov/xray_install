import asyncssh
import asyncio

from aiogram import Bot
from aiogram.types import Message


async def update_and_install_xray(ip, password):
    """
    Выполняет обновление системы, установку XRay, обновление геолокации и запуск XRay.

    :param ip: IP-адрес сервера
    :param password: Пароль для подключения
    :return: Строка с результатом выполнения операций
    """
    # Путь к локальному файлу конфигурации
    local_config_path = "/Users/evgenij/PycharmProjects/telegram_bot/media/send_media/config.json"
    # Путь на сервере, куда будет скопирован файл
    remote_config_path = "/usr/local/etc/xray/config.json"

    try:
        # Подключаемся к серверу
        async with asyncssh.connect(ip, username="root", password=password, known_hosts=None) as conn:
            # Обновление системы
            await conn.run("sudo apt update && sudo apt upgrade -y", check=True)

            # Установка XRay
            await conn.run(
                'bash -c "$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)" @ install --version v24.11.30',
                check=True
            )

            # Обновление геолокации
            await conn.run(
                'bash -c "$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)" @ install-geodata',
                check=True
            )

            # Копирование файла конфигурации на сервер
            await asyncssh.scp(local_config_path, (conn, remote_config_path))

            # Перезапуск XRay через systemctl
            await conn.run("sudo systemctl restart xray", check=True)
            await conn.run("sudo systemctl enable xray", check=True)

            # Проверяем статус сервиса
            result = await conn.run("sudo systemctl status xray", check=False)

            print(f"STDOUT: {result.stdout}")
            print(f"STDERR: {result.stderr}")

            await asyncio.sleep(5)

            # Перезагрузка сервера
            await conn.run('sudo reboot', check=True)

            if result.exit_status == 0:
                return f"✅ XRay успешно установлен, запущен и активирован на сервере {ip}."
            else:
                return f"⚠️ XRay установлен, но возникла ошибка при запуске: {result.stderr}"


    except asyncssh.Error as e:
        return f"Ошибка на сервере {ip}: {e}"


async def process_server(ip, password, message):
    """Обрабатывает один сервер и отправляет результат"""
    try:
        result = await update_and_install(ip, password)
        await message.answer(f"Сервер {ip}: {result}")
    except Exception as e:
        await message.answer(f"Ошибка на сервере {ip}: {str(e)}")


async def update_and_install(ip, password):
    """
    Выполняет обновление системы, установку XRay, обновление геолокации и запуск XRay.
    Возвращает строку с результатом выполнения операций.
    """

    try:
        # Подключаемся к серверу с увеличенным таймаутом
        async with asyncssh.connect(ip, username="root", password=password,
                                    connect_timeout=30, known_hosts=None) as conn:
            # Выполняем команды без ожидания завершения (если нужно)
            # await conn.run("reboot")
            await conn.run("sudo apt update && sudo apt upgrade -y", timeout=300)
            # await conn.run(
            #     'bash -c "$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)" @ remove')
            # Другие команды...

            return "Успешно обновлено и настроено"
    except Exception as e:
        raise Exception(f"SSH ошибка: {str(e)}")
