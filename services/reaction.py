import logging

import discord

from database.repositories.reaction_role import ReactionRoleRepository


class ReactionRoleService:
    def __init__(self, repository: ReactionRoleRepository, logger: logging.Logger):
        self.repository = repository
        self.logger = logger

    async def add_role(self, emoji: discord.Emoji, user: discord.Member):
        associated_role_id = self.repository.fetch_associated_role_id(emoji.name)
        if associated_role_id is None:
            self.logger.debug(f'Emoji "{emoji.name}" not associated with any role')
            return
        role = user.guild.get_role(associated_role_id)
        if role in user.roles:
            self.logger.warning(f'User {user.display_name} added reaction "{emoji.name}" '
                                f'on role message, but their role {role.name} did not change for '
                                f'they did have that role assigned already. '
                                f'Was it added manually?')
            return
        await user.add_roles(role)
        self.logger.info(f'User {user.display_name} receives role {role.name}'
                         f' in {user.guild.name} due to their reaction')

    async def remove_role(self, emoji: discord.Emoji, user: discord.Member):
        associated_role_id = self.repository.fetch_associated_role_id(emoji.name)
        if associated_role_id is None:
            self.logger.debug(f'Moji "{emoji.name}" not associated with any role')
            return
        role = user.guild.get_role(associated_role_id)
        if role not in user.roles:
            self.logger.warning(f'User {user.display_name} removed reaction "{emoji.name}" '
                                f'on role message, but their role {role.name} did not change for '
                                f'they did not have that role assigned already. '
                                f'Was it removed manually?')
            return
        await user.remove_roles(role)
        self.logger.info(f'User {user.display_name} loses role {role.name}'
                         f' in {user.guild.name} due to removal of their reaction')
