import logging

import discord

from database.repositories.commands import CommandsRepository
from database.repositories.helper import HelperRepository
from services.helper import HelperService
from services.role_channels import RoleChannels


class CommandService:
    def __init__(self,
                 command_repository: CommandsRepository,
                 helper_service: HelperService,
                 role_channels_service: RoleChannels,
                 logger: logging.Logger,
                 helper_repository: HelperRepository):
        self.repository = command_repository
        self.helper = helper_service
        self.role_channels = role_channels_service
        self.logger = logger
        self.helper_repository = helper_repository

    async def handle(self, message: discord.Message):
        guild: discord.Guild = message.guild
        simple_commands = self.repository.available_commands()
        command = message.content.split()[0][1:]

        self.logger.debug(f'content: {message.content}')
        if command in simple_commands:
            await message.reply(self.repository.response_for_command(command))
            return
        self.logger.debug('Simple command not recognized')

        if command == 'projekt':
            await self.role_channels.handle_project_channel(message)
            return
        
        if command == 'tech':
            await self.role_channels.handle_tech_channel(message)
            return
            