from aiogram import Bot
from aiogram.types import FSInputFile, CallbackQuery


from lexicon.lexicon import LEXICON
from config_data.config import ConfigFile, load_config_file
from aiogram.utils.i18n import gettext as _

path: ConfigFile = load_config_file()


async def send_media(file_id: int, user_id, bot: Bot):
    file = await select_file(file_id)
    document_bytes = FSInputFile(f'{path.file_pach.media_pach}{file.name}.conf')
    photo_bytes = FSInputFile(f'{path.file_pach.media_pach}{file.name}.png')
    # await bot.send_photo(chat_id=chat_id, photo=photo_bytes)
    await bot.send_document(chat_id=user_id, document=document_bytes,
                            caption=_("- это ваш <b>ключ</b>") + "\n\n" + _(LEXICON['/instruction']),
                            reply_markup=instruction_menu_pc)


async def send_media2(file_id: int, user_id, bot: Bot):
    file = await select_file(file_id)
    document_bytes = FSInputFile(f'{path.file_pach.media_pach}{file.name}.conf')
    photo_bytes = FSInputFile(f'{path.file_pach.media_pach}{file.name}.png')
    # await bot.send_photo(chat_id=chat_id, photo=photo_bytes)
    await bot.send_document(chat_id=user_id, document=document_bytes,
                            caption=_("- это ваш <b>ключ</b>"))


async def send_key(file_id: int, user_id, bot: Bot):
    file = await select_file(file_id)
    if file.country == 'DEU':
        country = '🇩🇪'
    elif file.country == 'USA':
        country = '🇺🇸'
    elif file.country == 'ENG':
        country = '🇬🇧'
    elif file.country == 'NLD':
        country = '🇳🇱'
    elif file.country == 'RUS':
        country = '🇷🇺'
    else:
        country = ''
    await bot.send_message(chat_id=user_id, text=_('Это ваш ключ, скопируйте его:'))
    if file.domain:
        await bot.send_message(chat_id=user_id,
                               text=f'vless://{file.uuid}@{file.domain}:443?security=reality&encryption=none&pbk=BhTJ3phnq-Z-10aFKSsj1lzhA8mULR4L6leE4-0WTAs&headerType=none&fp=chrome&spx=%2F&type=tcp&flow=xtls-rprx-vision&sni={file.sni}#{file.name}{country}')
    elif file.server:
        await bot.send_message(chat_id=user_id,
                               text=f'vless://{file.uuid}@{file.server}:443?security=reality&encryption=none&pbk=BhTJ3phnq-Z-10aFKSsj1lzhA8mULR4L6leE4-0WTAs&headerType=none&fp=chrome&spx=%2F&type=tcp&flow=xtls-rprx-vision&sni={file.sni}#{file.name}{country}')
    await bot.send_message(chat_id=user_id, text=_(LEXICON['/instruction']), reply_markup=instruction_menu_only_xray)


async def send_key2(file_id: int, user_id, bot: Bot):
    file = await select_file(file_id)
    if file.country == 'DEU':
        country = '🇩🇪'
    elif file.country == 'USA':
        country = '🇺🇸'
    elif file.country == 'ENG':
        country = '🇬🇧'
    elif file.country == 'NLD':
        country = '🇳🇱'
    elif file.country == 'RUS':
        country = '🇷🇺'
    else:
        country = ''
    await bot.send_message(chat_id=user_id, text=_('Это ваш ключ, скопируйте его:'))
    if file.domain:
        await bot.send_message(chat_id=user_id,
                               text=f'vless://{file.uuid}@{file.domain}:443?security=reality&encryption=none&pbk=BhTJ3phnq-Z-10aFKSsj1lzhA8mULR4L6leE4-0WTAs&headerType=none&fp=chrome&spx=%2F&type=tcp&flow=xtls-rprx-vision&sni={file.sni}#{file.name}{country}')
    elif file.server:
        await bot.send_message(chat_id=user_id,
                               text=f'vless://{file.uuid}@{file.server}:443?security=reality&encryption=none&pbk=BhTJ3phnq-Z-10aFKSsj1lzhA8mULR4L6leE4-0WTAs&headerType=none&fp=chrome&spx=%2F&type=tcp&flow=xtls-rprx-vision&sni={file.sni}#{file.name}{country}')


async def send_key_admin(file_id: int, user_id, bot: Bot):
    file = await select_file(file_id)
    if file.country == 'DEU':
        country = '🇩🇪'
    elif file.country == 'USA':
        country = '🇺🇸'
    elif file.country == 'ENG':
        country = '🇬🇧'
    elif file.country == 'NLD':
        country = '🇳🇱'
    elif file.country == 'RUS':
        country = '🇷🇺'
    else:
        country = ''
    await bot.send_message(chat_id=user_id, text=_('Это ваш ключ, скопируйте его:'))
    if file.server:
        await bot.send_message(chat_id=user_id,
                               text=f'vless://{file.uuid}@<code>{file.server}</code>:443?security=reality&encryption=none&pbk=BhTJ3phnq-Z-10aFKSsj1lzhA8mULR4L6leE4-0WTAs&headerType=none&fp=chrome&spx=%2F&type=tcp&flow=xtls-rprx-vision&sni={file.sni}#{file.name}{country}')
    if file.domain:
        domain_parts = file.domain.split('.', maxsplit=1)  # Разделяем только по первой точке
        domain_main = domain_parts[0]  # "deu47"
        domain_rest = domain_parts[1] if len(domain_parts) > 1 else ""  # "worldunlocker.org" (если есть)
        await bot.send_message(chat_id=user_id,
                               text=f'vless://{file.uuid}@<code>{domain_main}</code>.{domain_rest}:443?security=reality&encryption=none&pbk=BhTJ3phnq-Z-10aFKSsj1lzhA8mULR4L6leE4-0WTAs&headerType=none&fp=chrome&spx=%2F&type=tcp&flow=xtls-rprx-vision&sni={file.sni}#{file.name}{country}')
