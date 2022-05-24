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

        command = parse_command(message)

        self.logger.debug(f"Command '{command['name']}' recognized with arguments {command['args']} and parameters {command['params']}")


        if command['name'] in simple_commands:
            await message.reply(self.repository.response_for_command(command['name']))
            return
        self.logger.debug('Simple command not recognized')

<<<<<<< HEAD
        if command['name'].startswith('dziekuje'):
            self.logger.debug('Thank you command recognized')
            self.helper.handle_thankyou(message)
            return

        if command['name'] == 'ranking':
            self.logger.debug('Ranking command recognized')
            response = '\n'.join(
                [
                    f'{guild.get_member(rank.user_id)}\t has \t {rank.points} points'
                    for rank in self.helper_repository.get_whole_rank()
                ],
            ).strip()
            if not response:
                self.logger.debug('Reply not sent, because resulting response was empty')
                return
            await message.reply(response)

        if command['name'] in ['projekt', 'tech']:
            await self.role_channels.handle_role_channel(message, command)
=======
        if command == 'projekt':
            await self.role_channels.handle_project_channel(message)
>>>>>>> f691de8c9167ffd9493a33fbbf91555f1182e148
            return

        
def parse_command(message: discord.Message):
    command = message.content.split()[0][1:]
    arguments = message.content.split("-")[0].split()[1:]
    params = {p[0]:p[1:].split() for p in message.content.split("-")[1:]}
    return {
        'name': command,
        'args': arguments,
        'params': params,
    }