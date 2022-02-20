import logging

from database.repositories.helper import HelperRepository


class HelperService:
    def __init__(self, repository: HelperRepository, logger: logging.Logger):
        self.logger = logger
        self.repository = repository
