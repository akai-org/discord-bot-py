import database.repositories.commands


class CommandService:
    def __init__(self, command_repository: database.repositories.commands.CommandsRepository):
        self.repository = command_repository

    async def handle(self, message):
        available_commands = self.repository.available_commands()
        if message.content in available_commands:
            await message.reply(self.repository.response_for_command(message.content))