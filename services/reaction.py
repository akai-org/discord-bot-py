import logging

import discord

from database.repositories.reaction_role import MessageToRoleRepository


class MessageToRoleService:
    def __init__(self, repository: MessageToRoleRepository, logger: logging.Logger):
        self.repository = repository
        self.logger = logger

    async def add_role(self, message_id, user: discord.Member):
        if user.bot:
            self.logger.debug("Reaction received from a bot")
            return

        associated_role_id = self.repository.get_role_id(message_id)
        if associated_role_id is None:
            self.logger.debug(f'Message with ID "{message_id}" not associated with any role')
            return

        role = user.guild.get_role(associated_role_id)

        if role in user.roles:
            self.logger.warning(f'User {user.display_name} added reaction to a role message with ID '
                                f'{message_id}, but their role {role.name} did not change for '
                                f'they did have that role assigned already. '
                                f'Was it added manually?')
            return

        await user.add_roles(role)
        self.logger.info(f'User {user.display_name} receives role {role.name}'
                         f' in {user.guild.name} due to their reaction')

    async def remove_role(self, message_id, user: discord.Member):
        if user.bot:
            self.logger.debug("Reaction removed by a bot")
            return

        associated_role_id = self.repository.get_role_id(message_id)
        if associated_role_id is None:
            self.logger.debug(f'Message with ID "{message_id}" not associated with any role')
            return

        role = user.guild.get_role(associated_role_id)
        if role not in user.roles:
            self.logger.warning(f'User {user.display_name} removed reaction to a role message with ID '
                                f'{message_id}, but their role {role.name} did not change for '
                                f'they did not have that role assigned already. '
                                f'Was it removed manually?')
            return

        await user.remove_roles(role)
        self.logger.info(f'User {user.display_name} loses role {role.name}'
                         f' in {user.guild.name} due to removal of their reaction')
