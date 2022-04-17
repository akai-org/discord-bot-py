import logging

import discord

from database.repositories.commands import CommandsRepository
from database.repositories.helper import HelperRepository
from database.repositories.message_to_role import MessageToRoleRepository
from database.repositories.settings import SettingsRepository
from services.helper import HelperService
from services.util.request import RequestUtilService


class CommandService:
    def __init__(self,
                 command_repository: CommandsRepository,
                 settings_repo: SettingsRepository,
                 helper_service: HelperService,
                 logger: logging.Logger,
                 helper_repository: HelperRepository,
                 message_to_role_repository: MessageToRoleRepository,
                 request_util: RequestUtilService):
        self.repository = command_repository
        self.settings = settings_repo
        self.helper = helper_service
        self.logger = logger
        self.helper_repository = helper_repository
        self.message_to_role_repo = message_to_role_repository
        self.request_util = request_util

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

        if message.channel.id != int(self.settings.at_key('cli_channel_id')):
            self.logger.debug('Channel not recognized as subscribed')
            return

        if command == 'projekt':
            project_name = ''.join(message.content.split()[1:])

            if project_name == '':
                await message.reply('empty name')
                return

            self.logger.debug(f'New project named {project_name} recognized')
            project_channel_id = int(self.settings.at_key('project_channel_id'))

            if project_name not in guild.roles:
                role = await guild.create_role(name=project_name)

                url = f"/channels/{project_channel_id}/messages"
                data = {
                    "content": f'New project {project_name} appeared!'
                }
                response = self.request_util.make_post(data, url)

                self.message_to_role_repo.create_message_role_association(response['id'], role.id)

                channel = guild.get_channel(project_channel_id)
                await channel.get_partial_message(response['id']).add_reaction(self.settings.at_key('role_add_emoji'))
            else:
                await message.reply('project already exists')
