import logging

import discord

import database.repositories.settings
from database.repositories.message_to_role import MessageToRoleRepository
from database.repositories.helper import HelperRepository
from services.command import CommandService
from services.helper import HelperService
from services.message_to_role import MessageToRoleService
from services.thread import ThreadService


class AkaiBot(discord.Client):
    def __init__(self,
                 logger: logging.Logger,
                 settings_repo: database.repositories.settings.SettingsRepository,
                 command_service: CommandService,
                 message_to_role_service: MessageToRoleService,
                 message_to_role_repo: MessageToRoleRepository,
                 helper_service: HelperService,
                 helper_repo: HelperRepository,
                 thread_service: ThreadService
                 ):
        super().__init__(intents=discord.Intents.all())
        self.logger = logger
        self.settings = settings_repo
        self.command = command_service
        self.role_service = message_to_role_service
        self.role_repo = message_to_role_repo
        self.helper = helper_service
        self.helper_repo = helper_repo
        self.thread = thread_service

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

        if message.channel.id == int(self.settings.at_key('thread_channel_id')):
            self.logger.debug('Channel recognized as threads')
            await self.thread.new_thread(message)
            return

        if message.channel.id != int(self.settings.at_key('cli_channel_id')):
            self.logger.debug('Channel not recognized as subscribed')
            return

        if not message.content.startswith('$'):
            self.logger.debug('Message not recognized as command')
            return

        await self.command.handle(message)

    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        self.logger.debug('Received reaction add info')

        if self.role_repo.get_role_id(payload.message_id) is None:
            self.logger.debug('Received a reaction on a message not associated with any role')
            return

        if payload.emoji.name != self.settings.at_key('role_add_emoji'):
            self.logger.debug('Received a reaction emoji not allowed to grant roles')
            return

        self.logger.debug(f'User {payload.member.display_name} reacted with {payload.emoji.name} '
                          f'to message {payload.message_id}')

        await self.role_service.add_role(payload.message_id, payload.member)

        member = self.get_guild(payload.guild_id).get_member(payload.user_id)
        if payload.emoji.name in self.helper_repo.get_emojis():
            points = self.helper_repo.get_reward(payload.emoji.name)
            msg = await self.get_channel(payload.channel_id).fetch_message(payload.message_id)
            self.helper.add_points(msg.author, member, self.user, points)

    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        member = self.get_guild(payload.guild_id).get_member(payload.user_id)
        self.logger.debug('Received reaction remove info')

        if self.role_repo.get_role_id(payload.message_id) is None:
            self.logger.debug('Received a reaction removal on a message not associated with any role')
            return

        if payload.emoji.name != self.settings.at_key('role_add_emoji'):
            self.logger.debug('Received a reaction emoji removal not allowed to grant roles')
            return

        self.logger.debug(f'Reaction {payload.emoji.name} from user {member.display_name}'
                          f' to message {payload.message_id} has been cancelled')

        await self.role_service.remove_role(payload.message_id, member)

        if payload.emoji.name in self.helper_repo.get_emojis():
            points = self.helper_repo.get_reward(payload.emoji.name)
            msg = await self.get_channel(payload.channel_id).fetch_message(payload.message_id)
            self.helper.remove_points(msg.author, member, self.user, points)
