import sales_finder
import game_view
from settings_view import SettingsView
from embed import create_embed

import discord
from discord.ext import commands
from datetime import datetime

import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.typing = False
intents.message_content = True
intents.presences = False

class GameSalesBot(commands.Bot):
    def __init__(self, command_prefix, intents):
        super().__init__(command_prefix, intents=intents)

    async def on_ready(self):
        print('Bot is ready!')
        await self.change_presence(activity=discord.Game(name='+sales'))

    async def setup_hook(self):
        self.add_view(SettingsView())
        await super().setup_hook()

bot = GameSalesBot(command_prefix='+', intents=intents)

@bot.command()
async def settings(ctx: commands.Context):
    await ctx.send('Settings', view=SettingsView())

@bot.command()
async def sales(ctx: commands.Context, num_games = None):
    async with ctx.typing():
        sale_list = sales_finder.game_sales.fetch_sale_games(num_games, SettingsView.filtered_stores, SettingsView.only_aaa, SettingsView.on_sale, SettingsView.sort_by)

    view = game_view.GameListView(sale_list)
    bot.add_view(view)
    await ctx.send(embed=create_embed(sale_list[0]), view=view)

if __name__ == '__main__':
    bot.run(token=str(os.getenv('BOT_TOKEN')))
