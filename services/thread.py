import logging

import discord

from services.util.request import RequestUtilService


class ThreadService:
    def __init__(self, logger: logging.Logger, request_util: RequestUtilService):
        self.logger = logger
        self.request_util = request_util

    async def new_thread(self, message: discord.Message):
        self.logger.debug("Creating thread")
        await self.create_thread(name="Dyskusja", minutes=1440, message=message)

    async def create_thread(self, name, minutes, message):
        url = f"/channels/{message.channel.id}/messages/{message.id}/threads"
        data = {"name": name, "type": 11, "auto_archive_duration": minutes}
        return self.request_util.make_post(data, url)
