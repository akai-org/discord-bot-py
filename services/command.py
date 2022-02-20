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
        guild = message.guild
        simple_commands = self.repository.available_commands()
        trimmed_command = message.content[1:]
        if trimmed_command in simple_commands:
            await message.reply(self.repository.response_for_command(trimmed_command))
            return
        self.logger.debug('Simple command not recognized')
        if trimmed_command.startswith('dziekuje'):
            self.logger.debug('Thank you command recognized')
            self.helper.handle_thankyou(message)
            return
        if trimmed_command == 'ranking':
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

