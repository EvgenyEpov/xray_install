from dataclasses import dataclass

from environs import Env


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]



@dataclass
class Config:
    tg_bot: TgBot


def load_config(path: str | None = None):
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(
        token=env('BOT_TOKEN'),
        admin_ids=list(map(int, env.list('ADMIN_IDS')))))


@dataclass
class TgFile:
    media_pach: str
    config_pach: str


@dataclass
class ConfigFile:
    file_pach: TgFile


def load_config_file(path: str | None = None):
    env = Env()
    env.read_env(path)
    return ConfigFile(file_pach=TgFile(
        media_pach=env('MEDIA_PACH'),
        config_pach=env('CONFIG_PACH')))


@dataclass
class TgSSH:
    hosts: dict
    user: str
    port: int


@dataclass
class ConfigSSH:
    ssh_bot: TgSSH


def load_config_ssh(path: str | None = None):
    env = Env()
    env.read_env(path)
    return ConfigSSH(ssh_bot=TgSSH(
        hosts=env.dict("HOSTS", subcast=str),
        user=env('ROOT'),
        port=env.int('PORT')))
