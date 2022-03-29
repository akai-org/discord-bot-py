import logging

import discord

from database.repositories.commands import CommandsRepository
from database.repositories.helper import HelperRepository
from services.helper import HelperService


class CommandService:
    def __init__(self,
                 command_repository: CommandsRepository,
                 helper_service: HelperService,
                 logger: logging.Logger,
                 helper_repository: HelperRepository):
        self.repository = command_repository
        self.helper = helper_service
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

        if command.startswith('dziekuje'):
            self.logger.debug('Thank you command recognized')
            self.helper.handle_thankyou(message)
            return

        if command == 'ranking':
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

        if command == 'projekt':
            project_name = ''.join(message.content.split()[1:])
            if project_name == '':
                await message.reply('empty name')
                return

            self.logger.debug(f'New project named {project_name} recognized')

            if project_name in guild.roles:
                await message.reply('project already exists')
            else:
                await guild.create_role(name=project_name)
            await message.add_reaction('✅')
