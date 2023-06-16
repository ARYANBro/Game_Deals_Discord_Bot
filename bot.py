import sales_finder
import game_view

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

@bot.event
async def on_ready():
    print('Bot is ready!')

@bot.command()
async def embed(ctx, num_games = None):
    async with ctx.typing():
        sale_list = sales_finder.game_sales.fetch_sale_games(num_games)

        game = sale_list[0]
        initial_embed = discord.Embed(
            title=game['title'],
            description=game['description'],
            color=discord.Color.random(),
            timestamp=datetime.now()
        )

        initial_embed.set_footer(text="Footer text here")

        stores = sales_finder.game_sales.get_stores()
        store_logo_url = 'https://www.cheapshark.com' + stores[int(game['store_id']) - 1]['images']['logo']
        initial_embed.set_thumbnail(url=store_logo_url)
        initial_embed.set_image(url=game['game_cover'])

        initial_embed.add_field(name="Savings", value=str(int(float(game["savings"]))) + '%', inline=True)
        initial_embed.add_field(name="Store", value=sales_finder.game_sales.get_store_name(game["store_id"]), inline=True)
        initial_embed.add_field(name=f"", value=f"[**Buy Now!**]({game['store_link']})", inline=False)
        await ctx.send(embed=initial_embed, view=game_view.GameListView(sale_list, initial_embed))

if __name__ == '__main__':
    bot.run(token=str(os.getenv('BOT_TOKEN')))
