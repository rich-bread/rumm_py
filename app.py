import os
import discord
from discord.ext import commands

class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned, intents=discord.Intents().all())
        self.cogslist = ['get_map','post_map','go_integrate']

    async def setup_hook(self):
        if self.cogslist:
            for ext in self.cogslist:
                await self.load_extension(ext)

    async def on_ready(self):
        await self.tree.sync()

client = Client()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

client.run(TOKEN)