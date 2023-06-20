import sales_finder
import game_view
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

bot = commands.Bot(command_prefix='+', intents=intents)
filter_stores = []

class SettingsView(discord.ui.View):
    _select_options1 = []
    _select_options2 = []
    

    for i, store in enumerate(sales_finder.game_sales.get_stores()):
        if i == 25:
            break
        _select_options1.append(
            discord.SelectOption(
                label=store['storeName'],
                value=store['storeID'],
                emoji='🛒',
            )
        )
        
    for store in sales_finder.game_sales.get_stores()[25:]:
        _select_options2.append(
            discord.SelectOption(
                label=store['storeName'],
                value=store['storeID'],
                emoji='🛒',
            )
        )

    @discord.ui.select(placeholder='Filter options 1', min_values=1, max_values=len(_select_options1), options=_select_options1)
    async def filter_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        if select.values:
            filter_stores.extend(select.values)

        for select_option  in self._select_options1:
            select_option.default = False

        search_idx = 0
        for select_option in self._select_options1:

            if search_idx == len(select.values):
                break

            for value in select.values[search_idx:]:
                if value == select_option.value:
                    select_option.default = True
                    search_idx += 1
                    break

        await interaction.response.defer()

    @discord.ui.select(placeholder='Filter options 2', max_values=len(_select_options2), options=_select_options2)
    async def filter_select2(self, interaction: discord.Interaction, select: discord.ui.Select):
        if select.values:
            filter_stores.extend(select.values)

        for select_option  in self._select_options1:
            select_option.default = False

        search_idx = 0
        for select_option in self._select_options1:

            if search_idx == len(select.values):
                break

            for value in select.values[search_idx:]:
                if value == select_option.value:
                    select_option.default = True
                    search_idx += 1
                    break

        await interaction.response.defer()


@bot.event
async def on_ready():
    print('Bot is ready!')

@bot.command()
async def settings(ctx: commands.Context):
    await ctx.send('Settings', view=SettingsView())

@bot.command()
async def embed(ctx: commands.Context, num_games = None):
    async with ctx.typing():
        sale_list = sales_finder.game_sales.fetch_sale_games(num_games, filter_stores)

        game = sale_list[0]
        stores = sales_finder.game_sales.get_stores()

        initial_embed = create_embed(game, stores)

    await ctx.send(embed=initial_embed, view=game_view.GameListView(sale_list, initial_embed))

if __name__ == '__main__':
    bot.run(token=str(os.getenv('BOT_TOKEN')))
