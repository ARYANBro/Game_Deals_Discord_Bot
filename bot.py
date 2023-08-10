import sales_finder
import game_view
from settings_view import SettingsView
from embed import create_embed

import discord
from discord.ext import commands
import os
from discord import app_commands
from dotenv import load_dotenv
from isthereanydeal_api import ITAD_API
from cheapsharkapi import CheapSharkAPI
from api_locator import APILocator

GUILD_ID = discord.Object(id=1096429017114087474)

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

    async def setup_hook(self):
        SettingsView.init_class_attributes()
        self.add_view(SettingsView())
        await self.tree.sync(guild=GUILD_ID)
        await super().setup_hook()

bot = GameSalesBot(command_prefix='+', intents=intents)

@bot.tree.command(guild=GUILD_ID)
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message('Pong, latency {0} ms'.format(round(bot.latency * 1000, 2)))

@bot.tree.command(guild=GUILD_ID)
async def settings(interaction: discord.Interaction):
    try:
        await interaction.response.send_message('Using: {0}'.format(APILocator.get_api().__name__), view=SettingsView())
    except Exception as e:
        print(e)
        await interaction.response.send_message('Error ' + str(e))

@bot.tree.command(guild=GUILD_ID)
async def games(interaction: discord.Interaction, num_games: app_commands.Range[int, 1, 60]):
    try:
        await interaction.response.defer(thinking=True)
        sale_list = list(sales_finder.game_sales.fetch_sale_games(num_games, SettingsView.filtered_stores, SettingsView.selected_sort_options, **SettingsView.params))
        embeds = list(map(lambda game_info: create_embed(game_info), sale_list))
        view = game_view.GameListView(embeds)
        bot.add_view(view)
        await interaction.followup.send(embed=embeds[0], view=view)
    except Exception as e:
        print(e)
        await interaction.followup.send('Error ' + str(e))

@bot.tree.command(guild=GUILD_ID)
@app_commands.choices(api=[
    app_commands.Choice(name='IsThereAnyDeal', value=ITAD_API.__name__),
    app_commands.Choice(name='CheapShark', value=CheapSharkAPI.__name__),
])
async def switch_api(interaction: discord.Interaction, api: app_commands.Choice[str]):
    APILocator.provide_api(globals()[api.value])
    SettingsView.init_class_attributes()
    await interaction.response.send_message('API switched to ' + api.name)

if __name__ == '__main__':
    bot.run(token=str(os.getenv('BOT_TOKEN')))
 