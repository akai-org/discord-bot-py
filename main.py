import sys
from logging import Logger
import os
from dotenv import load_dotenv
import logging
import database.repositories.settings
import services.command
from akaibot import AkaiBot
from database.models.command import Command
from database.models.setting import Setting
from database.orm import Session
from database.repositories.commands import CommandsRepository

ENV_BOT_TOKEN = 'TOKEN'
ENV_LOG_FILE = 'LOGFILE'
WRITE_FILE_MODE = 'w'
LOG_FILE_ENCODING = 'utf-8'
DISCORD_LIB_LOGGER_NAME = 'discord'
BOT_LOGGER_NAME = 'akaibot'
LOGGER_FORMATTING = '%(asctime)s %(levelname)s %(name)s: %(message)s'
#

# env
load_dotenv()
LOG_FILE = os.getenv(ENV_LOG_FILE)
TOKEN = os.getenv(ENV_BOT_TOKEN)
#

# discord lib logger
discord_lib_logger: Logger = logging.getLogger(DISCORD_LIB_LOGGER_NAME)
discord_lib_logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(filename=LOG_FILE, encoding=LOG_FILE_ENCODING, mode=WRITE_FILE_MODE)
file_handler.setFormatter(logging.Formatter(LOGGER_FORMATTING))
discord_lib_logger.addHandler(file_handler)
#

# akai bot logger
logger: Logger = logging.getLogger(BOT_LOGGER_NAME)
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(logging.Formatter(LOGGER_FORMATTING))
logger.addHandler(console_handler)
#


if __name__ == '__main__':
    settings_repository = database.repositories.settings.SettingsRepository(
        sessionmaker=Session,
        model=Setting
    )
    command_repository = CommandsRepository(
        sessionmaker=Session,
        model=Command
    )
    command_service = services.command.CommandService(command_repository)
    bot = AkaiBot(logger,
                  settings_repository,
                  command_service
                  )
    bot.run(TOKEN)
