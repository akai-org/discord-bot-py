import logging

import discord

from database.repositories.helper import HelperRepository


class HelperService:
    def __init__(self, repository: HelperRepository, logger: logging.Logger):
        self.logger = logger
        self.repository = repository

    def handle_thankyou(self, message: discord.Message):
        thanked_users: list[discord.Member] = message.mentions
        for user in thanked_users:
            self.repository.add_points_to_user(user.id, 1)
            self.logger.info(f'User {user.display_name} got {1} point from '
                             f'{message.author.display_name} for being helpful')
