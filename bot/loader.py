import configparser
from dataclasses import dataclass


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str


@dataclass
class TgBot:
    token: str
    admin_id: int
    use_redis: bool


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig


def load_config(path: str):
    config = configparser.ConfigParser()
    config.read(path)

    bot = config["bot"]

    return Config(
        tg_bot=TgBot(
            token=bot.get("token"),
            admin_id=bot.getint("admin_id"),
            use_redis=bot.getboolean("use_redis"),
        ),
        db=DbConfig(**config["db"]),
    )