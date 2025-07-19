from aiogram import Bot
from aiogram.types import BotCommand

from lexicon.lexicon import LEXICON_COMMANDS_EN, LEXICON_COMMANDS_RU, LEXICON_COMMANDS_FA


async def set_main_menu(bot: Bot):
    main_menu_commands_ru = [BotCommand(
        command=command,
        description=description
    ) for command,
    description in LEXICON_COMMANDS_RU.items()]

    main_menu_commands_en = [BotCommand(
        command=command,
        description=description
    ) for command,
    description in LEXICON_COMMANDS_EN.items()]

    main_menu_commands_fa = [BotCommand(
        command=command,
        description=description
    ) for command, description in LEXICON_COMMANDS_FA.items()]

    await bot.set_my_commands(main_menu_commands_ru, language_code='ru')
    await bot.set_my_commands(main_menu_commands_ru, language_code='be')
    await bot.set_my_commands(main_menu_commands_fa, language_code='fa')
    await bot.set_my_commands(main_menu_commands_en)
