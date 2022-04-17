import logging
import os
import sys
from logging import Logger

from dotenv import load_dotenv

import database.repositories.settings
import log_handling
from akaibot import AkaiBot
from database.models.command import Command
from database.models.helper_rank import HelperRank
from database.models.helper_rank_threshold import HelperRankThreshold
from database.models.message_to_role import MessageToRole
from database.models.setting import Setting
from database.orm import Session
from database.repositories.commands import CommandsRepository
from database.repositories.helper import HelperRepository
from database.repositories.message_to_role import MessageToRoleRepository
from services.command import CommandService
from services.helper import HelperService
from services.message_to_role import MessageToRoleService
from services.thread import ThreadService
from services.util.request import RequestUtilService

WRITE_FILE_MODE = 'w'
LOG_FILE_ENCODING = 'utf-8'
DISCORD_LIB_LOGGER_NAME = 'discord'
BOT_LOGGER_NAME = 'akaibot'
LOGGER_FORMATTING = '%(asctime)s %(levelname)s %(name)s: %(message)s'
#

# env
load_dotenv()
LOG_FILE = os.getenv('LOGFILE')
TOKEN = os.getenv('TOKEN')
DISCORD_LOG_CHANNEL_ID = os.getenv('DISCORD_LOG_CHANNEL_ID')
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
console_handler.setLevel(logging.DEBUG)
logger.addHandler(console_handler)
#


if __name__ == '__main__':
    # repositories
    settings_repository = database.repositories.settings.SettingsRepository(
        sessionmaker=Session,
        model=Setting
    )
    command_repository = CommandsRepository(
        sessionmaker=Session,
        model=Command
    )
    message_to_role_repository = MessageToRoleRepository(
        sessionmaker=Session,
        model=MessageToRole
    )
    helper_repository = HelperRepository(
        sessionmaker=Session,
        user_rank_model=HelperRank,
        helper_range_model=HelperRankThreshold
    )

    # services
    request_util = RequestUtilService(TOKEN)
    message_to_role_service = MessageToRoleService(message_to_role_repository, logger)
    helper_service = HelperService(helper_repository, logger)
    command_service = CommandService(command_repository, settings_repository, helper_service, logger, helper_repository,
                                     message_to_role_repository, request_util)
    thread_service = ThreadService(logger, request_util)

    bot = AkaiBot(logger, settings_repository, command_service, message_to_role_service, message_to_role_repository,
                  helper_service, thread_service)

    if DISCORD_LOG_CHANNEL_ID is not None:
        discord_handler = log_handling.DiscordHandler(bot, int(DISCORD_LOG_CHANNEL_ID))
        discord_handler.setLevel(logging.INFO)
        discord_handler.setFormatter(logging.Formatter(LOGGER_FORMATTING))
        logger.addHandler(discord_handler)

    bot.run(TOKEN)
