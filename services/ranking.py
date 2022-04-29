import logging
import discord
from datetime import datetime
from database.repositories.commands import CommandsRepository
from database.repositories.helper import HelperRepository


class RankingService:
    def __init__(self,
                 logger: logging.Logger,
                 command_repository: CommandsRepository,
                 helper_repository: HelperRepository):
        self.logger = logger
        self.repository = command_repository
        self.helper_repository = helper_repository

    async def update(self):
        if not hasattr(self, 'anchor'):
            self.logger.debug('Ranking has not been set up.')
            return
        info = ''
        place = 1
        for rank in self.helper_repository.get_whole_rank():
            if not hasattr(self.guild.get_member(rank.user_id), 'name') or rank.points == 0:
                continue
            info += (f'{":first_place:" if place == 1 else ":second_place:" if place == 2 else ":third_place:" if place == 3 else "`"+str(place)+".`"} '
                     f'**{self.guild.get_member(rank.user_id).name}** — {rank.points} {"point" if rank.points == 1 else "points"}\n')
            place += 1
        embed = discord.Embed(title = '\n', description = info, color=0xFAA21B, timestamp=datetime.now())
        embed.set_author(name = 'RANKING:')
        embed.set_thumbnail(url = '')     # można dodać zdjęcie
        embed.set_footer(text = 'Last updated', icon_url = 'https://i.imgur.com/T6PhftD.png')
        await self.anchor.edit(content = '** **', embed = embed)

    async def setup(self, bot, message: discord.Message):
        if message.content == "$setup":
            self.channel = message.channel
            self.logger.debug('Setting up the ranking...')
            await message.delete()
            await self.channel.send('Loading...')

        if message.author == bot.user:
            self.anchor = message
            self.guild = message.guild
            self.logger.debug('Ranking has been set up.')
            await self.update()
        
