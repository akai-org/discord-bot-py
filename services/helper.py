import logging

import discord

from database.repositories.helper import HelperRepository


class HelperService:
    def __init__(self, repository: HelperRepository, logger: logging.Logger):
        self.logger = logger
        self.repository = repository

    def add_points(self, thanked, thanker, bot, p):
        if thanked not in {thanker, bot}:
            self.repository.add_points_to_user(thanked.id, p)
            self.logger.debug(f'User {thanked.display_name} got {p} point{"" if p == 1 else "s"} from '
                              f'{thanker.display_name} for being helpful')
        else:
            self.logger.debug(f'User {thanker.display_name} cannot thank '
                              f'{thanked.display_name}')

    def remove_points(self, thanked, thanker, bot, p):
        if thanked not in {thanker, bot}:
            self.repository.add_points_to_user(thanked.id, -p)
            self.logger.debug(f'User {thanked.display_name} lost {p} point{"" if p == 1 else "s"} from '
                              f'{thanker.display_name}')
        else:
            self.logger.debug(f'User {thanker.display_name} cannot thank '
                              f'{thanked.display_name} *')
