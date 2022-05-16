import logging

import requests
import asyncio
from ics import Calendar
from discord.ext import tasks
from datetime import datetime, timezone

from database.repositories.settings import SettingsRepository
from services.util.request import RequestUtilService

class EventService:
    def __init__(self, 
                 logger: logging.Logger, 
                 settings_repo: SettingsRepository,
                 request_util: RequestUtilService):
        self.logger = logger
        self.settings = settings_repo
        self.request_util = request_util
        self.calendar_url = self.settings.at_key('calendar_url')
        
    @tasks.loop(hours=24)
    async def auto_update(self, guild_id):
        event_url = f'/guilds/{guild_id}/scheduled-events'
        cal = Calendar(requests.get(self.calendar_url).text)
        calendar_events = sorted(cal.events)
        discord_events = self.request_util.make_get(event_url)

        for event in calendar_events:
            if self.is_new(event, discord_events):
                data = {
                'name': event.name,
                'privacy_level': 2,
                'scheduled_start_time': event.begin.strftime("%Y-%m-%dT%H:%M:%S"),
                'scheduled_end_time': event.end.strftime("%Y-%m-%dT%H:%M:%S"),
                'description': event.description,
                'channel_id': None,
                'entity_metadata': {'location': event.location if event.location else 'Unknown'},
                'entity_type': 3
                }
                await self.create_event(data, event_url)


    async def create_event(self, data, url):
        result = self.request_util.make_post(data, url)
        if 'retry_after' in result:
            await asyncio.sleep(int(result['retry_after'])+1)
            return await self.create_event(data, url)
        else:
            self.logger.debug(f'Event created: {result["name"]}')
            return result
    

    def is_new(self, new_event, present_events):
        if new_event.begin < datetime.now(timezone.utc):
            return False
        for event in present_events:
            if event['name'] == new_event.name and event['scheduled_start_time'] == new_event.begin.strftime("%Y-%m-%dT%H:%M:%S+00:00"):
                return False
        return True
