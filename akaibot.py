import logging

import discord

import database.repositories.settings
from services.command import CommandService
from services.helper import HelperService
from services.reaction import ReactionRoleService


class AkaiBot(discord.Client):
    def __init__(self,
                 logger: logging.Logger,
                 settings_repo: database.repositories.settings.SettingsRepository,
                 command_service: CommandService,
                 reaction_role_service: ReactionRoleService,
                 helper_service: HelperService
                 ):
        super().__init__(intents=discord.Intents.all())
        self.logger = logger
        self.settings = settings_repo
        self.command = command_service
        self.reaction = reaction_role_service
        self.helper = helper_service

    async def on_ready(self):
        self.logger.info(f'Bot is ready to use, logged in as {self.user}')

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            self.logger.debug('Recognized self as message author')
            return

        if isinstance(message.channel, discord.DMChannel) or isinstance(message.channel, discord.GroupChannel):
            self.logger.debug(f'Private message received from {message.author}: {message.content}')
            await message.reply(self.settings.at_key('priv_response'))
            return

        self.logger.debug(f'Received message sent on '
                          f'{message.channel.name} in {message.channel.category.name} in '
                          f'{message.channel.guild.name}')

        if message.channel.id != int(self.settings.at_key('bot_channel_id')):
            self.logger.debug('Channel not recognized as subscribed')
            return

        if not message.content.startswith('$'):
            self.logger.debug('Message not recognized as command')
            return

        await self.command.handle(message)

    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        self.logger.debug('Recived reaction add info')
        if payload.message_id != int(self.settings.at_key('reaction_role_message_id')):
            self.logger.debug('Reaction message is not recognized as subscribed')
            return
        self.logger.debug(f'User {payload.member.display_name} reacted with {payload.emoji.name} '
                          f'to message {payload.message_id}')
        await self.reaction.add_role(payload.emoji, payload.member)

    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        member = self.get_guild(payload.guild_id).get_member(payload.user_id)
        self.logger.debug('Recived reaction remove info')
        if payload.message_id != int(self.settings.at_key('reaction_role_message_id')):
            self.logger.debug('Reaction message is not recognized as subscribed')
            return
        self.logger.debug(f'Reaction {payload.emoji.name} from user {member.display_name}'
                          f' to message {payload.message_id} has been cancelled ')
        await self.reaction.remove_role(payload.emoji, member)
