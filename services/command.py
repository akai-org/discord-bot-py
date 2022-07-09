import logging

import discord

from database.repositories.commands import CommandsRepository
from database.repositories.helper import HelperRepository
from services.helper import HelperService
from services.role_channels import RoleChannels


class CommandService:
    def __init__(
        self,
        command_repository: CommandsRepository,
        helper_service: HelperService,
        role_channels_service: RoleChannels,
        logger: logging.Logger,
        helper_repository: HelperRepository,
    ):
        self.repository = command_repository
        self.helper = helper_service
        self.role_channels = role_channels_service
        self.logger = logger
        self.helper_repository = helper_repository

    async def handle(self, message: discord.Message):
        guild: discord.Guild = message.guild
        simple_commands = self.repository.available_commands()

        command = full_command(message)

        self.logger.debug(
            f"Command '{command['name']}' recognized with arguments {command['args']} and parameters {command['params']}"
        )

        if command["name"] in simple_commands:
            await message.reply(self.repository.response_for_command(command["name"]))
            return
        self.logger.debug("Simple command not recognized")

        if command["name"] in ["projekt", "tech"]:
            await self.role_channels.handle_role_channel(message, command)
            return


def full_command(message: discord.Message):
    command = message.content.split()[0][1:]
    arguments = message.content.split(" -")[0].split()[1:]
    params = {p[0]: p[1:].split() for p in message.content.split(" -")[1:]}
    return {"name": command, "args": arguments, "params": params}
