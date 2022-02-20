import logging
import discord

import database.repositories.settings
import services.command


class AkaiBot(discord.Client):
    def __init__(self,
                 logger: logging.Logger,
                 settings_repo: database.repositories.settings.SettingsRepository,
                 command_service: services.command.CommandService
                 ):
        super().__init__(intents=discord.Intents.all())
        self.logger = logger
        self.settings = settings_repo
        self.command = command_service

    async def on_ready(self):
        self.logger.info(f'Bot is ready to use, logged in as {self.user}')

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            self.logger.debug('Recognized self as message author')
            return

        if isinstance(message.channel, discord.DMChannel) or isinstance(message.channel, discord.GroupChannel):
            self.logger.info(f'Private message received from {message.author}: {message.content}')
            await message.reply(self.settings.at_key('priv_response'))
            return

        self.logger.info(f'Received message sent on '
                         f'{message.channel.name} in {message.channel.category.name} in '
                         f'{message.channel.guild.name}')

        if message.channel.id != int(self.settings.at_key('bot_channel_id')):
            self.logger.debug('Channel not recognized as subscribed')
            return

        await self.command.handle(message)

