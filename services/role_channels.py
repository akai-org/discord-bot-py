from distutils.log import debug
import discord
import logging

from database.repositories.settings import SettingsRepository
from database.repositories.message_to_role import MessageToRoleRepository
from services.util.request import RequestUtilService

ROLE_TYPES = {
    'projekt': {'name': 'project', 'id': 'project_channel_id'},
    'tech': {'name': 'technology', 'id': 'technology_channel_id'},
}

class RoleChannels:
    def __init__(self,
                 logger: logging.Logger,
                 settings_repo: SettingsRepository,
                 message_to_role_repository: MessageToRoleRepository,
                 request_util: RequestUtilService):
        self.logger = logger
        self.settings = settings_repo
        self.message_to_role_repo = message_to_role_repository
        self.request_util = request_util


    async def handle_role_channel(self, message, command):
        if len(command["args"]) == 0:
            await message.reply(f'USAGE: \n\t{command["name"]} <role_names>\t      - to create roles \n\t{command["name"]} <role_names> -d\t - to delete roles')

        for role_name in command['args']:
            if len(command['params']) == 0:
                await self.create_role_channel(message, command, role_name)
            elif "d" in command['params']:
                await self.delete_role_channel(message, command, role_name)


    async def create_role_channel(self, message, command, role_name):
        guild = message.guild
    
        role_type = ROLE_TYPES[command["name"]]["name"]

        self.logger.debug(f'New {role_type} named {role_name} recognized')
        channel_id = int(self.settings.at_key(ROLE_TYPES[command["name"]]['id']))

        if role_name not in [x.name for x in guild.roles]:
            role = await guild.create_role(name=role_name)

            url = f"/channels/{channel_id}/messages"
            data = {
                "content": f'New {role_type} {role_name} appeared!'
            }
            response = self.request_util.make_post(data, url)

            self.message_to_role_repo.create_message_role_association(response['id'], role.id)

            channel = guild.get_channel(channel_id)
            await channel.get_partial_message(response['id']).add_reaction(self.settings.at_key('role_add_emoji'))
        else:
            await message.reply(f'{role_type} - {role_name} already exists')

    
    async def delete_role_channel(self, message, command, role_name):
        guild = message.guild
        channel_id = int(self.settings.at_key(ROLE_TYPES[command["name"]]['id']))
        channel = guild.get_channel(channel_id)
        messages = await channel.history(limit=1000).flatten()
        for m in messages:
            if(role_name in m.content.split()):
                self.logger.debug(f'Deleting {role_name} from {channel.name}')
                await m.delete()

                role_type = ROLE_TYPES[command["name"]]["name"]
                role_object = discord.utils.get(guild.roles, name=role_name) 
                await role_object.delete()

                await message.reply(f'Deleted {role_type} - {role_name}')
                break
        else:
            await message.reply(f'{role_name} not found in {channel.name}')

