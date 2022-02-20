import asyncio
from logging import StreamHandler

import discord


class DiscordHandler(StreamHandler):
    def __init__(self, client: discord.Client, channel_id: int):
        super().__init__()
        self.client = client
        self.channel_id = channel_id

    def emit(self, record):
        msg = self.format(record)
        asyncio.create_task(self.client.get_channel(self.channel_id).send(msg))
