import logging

import discord

from database.repositories.helper import HelperRepository


class HelperService:
    def __init__(self, repository: HelperRepository, logger: logging.Logger):
        self.logger = logger
        self.repository = repository

    async def change_points(self, thanked, thanker, bot, p):
        if thanked not in {thanker, bot}:
            self.repository.add_points_to_user(thanked.id, p)
            role_id = self.repository.role_id_user_should_have(thanked.id)
            await self.change_roles(thanked, role_id)
            self.logger.debug(
                f'User {thanked.display_name} {"lost" if p < 0 else "got"} {abs(p)} point{"" if abs(p) == 1 else "s"} from '
                f"{thanker.display_name}"
            )
        else:
            self.logger.debug(f"User {thanker.display_name} cannot thank " f"{thanked.display_name}")

    async def change_roles(self, user, role_id):
        for role in self.repository.get_roles():
            if role == role_id:
                continue
            await user.remove_roles(discord.utils.get(user.guild.roles, id=role))
        if role_id is not None:
            await user.add_roles(discord.utils.get(user.guild.roles, id=role_id))
