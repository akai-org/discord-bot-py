import requests
import logging
import discord


class ThreadService:
    def __init__(self, logger: logging.Logger):
        self.logger = logger

    async def create_thread(self,name,minutes,message):
        token = 'Bot ' + self._state.http.token
        url = f"https://discord.com/api/v9/channels/{self.id}/messages/{message.id}/threads"
        headers = {
            "authorization" : token,
            "content-type" : "application/json"
        }
        data = {
            "name" : name,
            "type" : 11,
            "auto_archive_duration" : minutes
        }
        return requests.post(url,headers=headers,json=data).json()

    discord.TextChannel.create_thread = create_thread
    
    async def new_thread(self, message: discord.Message):
        self.logger.debug('Creating thread')
        f = await message.channel.create_thread(name="Dyskusja", minutes=1440, message=message)
        return
