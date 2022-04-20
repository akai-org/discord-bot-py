import logging

from database.repositories.settings import SettingsRepository
from database.repositories.message_to_role import MessageToRoleRepository
from services.util.request import RequestUtilService

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

    async def handle_project_channel(self, message):
        guild = message.guild
        project_name = ''.join(message.content.split()[1:])
        if project_name == '':
            await message.reply('empty name')
            return

        self.logger.debug(f'New project named {project_name} recognized')
        project_channel_id = int(self.settings.at_key('project_channel_id'))

        if project_name not in [x.name for x in guild.roles]:
            role = await guild.create_role(name=project_name)

            url = f"/channels/{project_channel_id}/messages"
            data = {
                "content": f'New project {project_name} appeared!'
            }
            response = self.request_util.make_post(data, url)

            self.message_to_role_repo.create_message_role_association(response['id'], role.id)

            channel = guild.get_channel(project_channel_id)
            await channel.get_partial_message(response['id']).add_reaction(self.settings.at_key('role_add_emoji'))
        else:
            await message.reply('project already exists')